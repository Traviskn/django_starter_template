from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpRequest
from social.pipeline.partial import partial
from social.exceptions import InvalidEmail


# See: http://psa.matiasaguirre.net/docs/pipeline.html#partial-pipeline
@partial
def request_user_email(backend, details, response, user=None, is_new=False, *args, **kwargs):
    if is_new and details.get('email') == '':
        data = backend.strategy.request_data()
        if data.get('email') is None:
            return render_to_response('accounts/social_auth_request_email.html')
        else:
            details['email'] = data.get('email')


@partial
def mail_validation(backend, details, is_new=False, *args, **kwargs):
    requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)
    send_validation = details.get('email') and \
                      (is_new or backend.setting('PASSWORDLESS', False))
    if requires_validation and send_validation:
        data = backend.strategy.request_data()
        if 'verification_code' in data:
            backend.strategy.session_pop('email_validation_address')
            if not backend.strategy.validate_email(details['email'],
                                           data['verification_code']):
                raise InvalidEmail(backend)
            else:
                if not backend.strategy.request:
                    backend.strategy.request = HttpRequest
                messages.add_message(backend.strategy.request, messages.SUCCESS, 'Email successfully validated!')
        else:
            backend.strategy.send_email_validation(backend, details['email'])
            backend.strategy.session_set('email_validation_address',
                                         details['email'])
            return backend.strategy.redirect(
                backend.strategy.setting('EMAIL_VALIDATION_URL')
            )

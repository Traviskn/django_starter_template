# See: https://docs.djangoproject.com/en/1.8/topics/auth/default/#using-the-views
from django.contrib.auth import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from .models import User, SecurityDetails
from .forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserProfileForm


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.verify_user_email(request)
            return render(request, 'accounts/email_verification_sent.html', {})

    context = {'form': form}
    context.update(csrf(request))
    return render(request, 'accounts/register.html', context)


def verify_email(request, email, token):
    valid_link = False

    try:
        user = User.objects.get(email=email)
        security_details = SecurityDetails.objects.get(user=user)
        if security_details.is_token_valid(token):
            user.is_active = True
            valid_link = True
    except User.DoesNotExist:
        pass  # simply means an invalid link
    except SecurityDetails.DoesNotExist:
        pass  # simply means an invalid link

    # allow the user to request another verification email
    if request.method == 'POST':
        email = request.POST.get('email', None)
        try:
            user = User.objects.get(email=email)
            user.verify_user_email(request)
        except User.DoesNotExist:
            pass  # for security, don't expose which emails we have or don't have in the system
        return render(request, 'accounts/email_verification_sent.html', {})

    context = {'valid_link': valid_link}
    context.update(csrf(request))
    return render(request, 'accounts/email_verification_confirm.html', context)


def verification_sent(request):
    return render_to_response('accounts/email_verification_sent.html')


# See: http://python-social-auth.readthedocs.org/en/latest/pipeline.html#email-validation
def social_auth_validate_email(strategy, backend, code):
    url = strategy.build_absolute_uri(
        reverse('social:complete', args=(backend.name,))
    ) + '?verification_code=' + code.code
    subject = 'Please Validate Your Email'
    message = 'Thank you for registering!  Please follow the link below to verify your email: \n' + url
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [code.email], fail_silently=False)


def login(request):
    return views.login(
        request,
        template_name='accounts/login.html',
        # redirect_field_name='next',
        authentication_form=AuthenticationForm,
        # current_app=None,
        extra_context=csrf(request)
    )


@login_required()
def logout(request):
    return views.logout(
        request,
        next_page='/'
        # template_name='registration/logged_out.html',
        # redirect_field_name='next',
        # current_app=None,
        # extra_context={}
    )


@login_required()
def profile(request):
    form = UserProfileForm(instance=request.user)

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile successfully updated.')

    context = {
        'form': form
    }
    return render(request, 'accounts/profile.html', context)


@login_required()
def password_change(request):
    # Allows a user to change their password.
    return views.password_change(
        request,
        template_name='accounts/password_change_form.html',
        post_change_redirect=reverse('accounts:password_change_done'),
        password_change_form=PasswordChangeForm,
        # current_app=None,
        # extra_context={}
    )


@login_required()
def password_change_done(request):
    # The page shown after a user has changed their password.
    return views.password_change_done(
        request,
        template_name='accounts/password_change_done.html'
        # current_app=None,
        # extra_context={}
    )


def password_reset(request):
    # Allows a user to reset their password by generating a one-time use link that can be used to reset the password,
    # and sending that link to the user’s registered email address.
    return views.password_reset(
        request,
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        # subject_template_name='registration/password_reset_subject.txt',
        password_reset_form=PasswordResetForm,
        # token_generator=default_token_generator,
        post_reset_redirect=reverse('accounts:password_reset_done')
        # from_email=DEFAULT_FROM_EMAIL,
        # current_app=None,
        # extra_context={},
        # html_email_template_name=None
    )


def password_reset_done(request):
    # The page shown after a user has been emailed a link to reset their password.
    return views.password_reset_done(
        request,
        template_name='accounts/password_reset_done.html',
        # current_app=None,
        # extra_context={}
    )


def password_reset_confirm(request, uidb64=None, token=None):
    # Allows a user to change their password without entering in their old one.
    # Used after confirming a password reset link.
    return views.password_reset_confirm(
        request,
        uidb64=uidb64,
        token=token,
        template_name='accounts/password_reset_confirm.html',
        # token_generator=default_token_generator,
        set_password_form=SetPasswordForm,
        post_reset_redirect=reverse('accounts:password_reset_complete'),
        # current_app=None,
        # extra_context={}
    )


def password_reset_complete(request):
    # Presents a view which informs the user that the password has been successfully changed.
    return views.password_reset_complete(
        request,
        template_name='accounts/password_reset_complete.html'
        # current_app=None,
        # extra_context={}
    )

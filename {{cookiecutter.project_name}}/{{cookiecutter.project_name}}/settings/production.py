"""
Django production settings for {{cookiecutter.project_name}}.
See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
"""

from .common import *

# ######### SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key
# Set SECRET_KEY environment variable on the production machine.
SECRET_KEY = get_env_setting('SECRET_KEY')
# ######### END SECRET CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_USE_TLS = get_env_setting('EMAIL_USE_TLS')
EMAIL_HOST = get_env_setting('EMAIL_HOST')
EMAIL_PORT = get_env_setting('EMAIL_PORT')
EMAIL_HOST_USER = get_env_setting('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_setting('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_setting('DEFAULT_FROM_EMAIL')
DEFAULT_TO_EMAIL = get_env_setting('DEFAULT_TO_EMAIL')
# ######### END EMAIL CONFIGURATION


# ######### STORAGES CONFIGURATION
# Use Amazon S3 for user uploaded media.
# See: https://github.com/jschneier/django-storages
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = '{{cookiecutter.project_name}}.custom_storages.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
# ######### END STORAGES CONFIGURATION


# ######### WEBPACK LOADER CONFIGURATION
# See: https://github.com/owais/django-webpack-loader
WEBPACK_LOADER = {
    'BUNDLE_DIR_NAME': 'deploy/',
    'STATS_FILE': os.path.join(BASE_DIR, "webpack/webpack-stats-prod.json"),
}
# ######### END WEBPACK LOADER CONFIGURATION


# ########## CDN CONFIGURATION
# Optionally use a CDN.
# See: http://whitenoise.readthedocs.org/en/latest/django.html#use-a-content-delivery-network-optional
STATIC_HOST = os.environ.get('CDN_URL', '')
STATIC_URL = STATIC_HOST + '/static/'
# ########## END CDN CONFIGURATION


# ########## HEROKU DEPLOYMENT SETTINGS
# These are Heroku deployment settings, uncomment the lines below to use them
# see https://devcenter.heroku.com/articles/getting-started-with-django#django-settings

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
# ########## END HEROKU SETTINGS

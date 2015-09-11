"""
Django settings for {{cookiecutter.project_name}}.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


# ######### PATH CONFIGURATION
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ######### END PATH CONFIGURATION


# ######### ENVIRONMENT VARIABLES CONFIGURATION
# Some configuration settings, such as the secret key, database password, etc.
# should be kept out of our code and version control. Instead, we will keep
# them in environment variables.

from django.core.exceptions import ImproperlyConfigured
def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

# We can optionally use a .env text file in the project root to configure
# environment variables.  The .env file should not be tracked in version control.
# See: https://github.com/theskumar/python-dotenv
from dotenv import load_dotenv
DOTENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(DOTENV_PATH)
# ######### END ENVIRONMENT VARIABLES CONFIGURATION


# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#debug
DEBUG = False
# ######### END DEBUG CONFIGURATION


# ######### APPLICATION DEFINITION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#installed-apps
INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'accounts',
)
# ######### END APPLICATION DEFINITION


# ######### MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
# ######### END MIDDLEWARE CONFIGURATION


# ######### URL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#root-urlconf
ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'
# ######### END URL CONFIGURATION


# ######### TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
# ######### END TEMPLATE CONFIGURATION


# ######### WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#wsgi-application
WSGI_APPLICATION = '{{cookiecutter.project_name}}.wsgi.application'
# ######### END WSGI CONFIGURATION


# ######### ADMIN CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#admins
# When DEBUG=False and a view raises an exception,
# Django will email these people with the full exception information.
ADMINS = (
    ('Travis Nuttall', 'tuttall@gmail.com'),
)

# See: https://docs.djangoproject.com/en/1.8/ref/settings/#managers
MANAGERS = ADMINS
# ######### END ADMIN CONFIGURATION


# ######### DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Load database configuration from the DATABASE_URL environment variable.
# See: https://github.com/kennethreitz/dj-database-url
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Enable Connection Pooling.
# See: https://github.com/kennethreitz/django-postgrespool
DATABASES['default']['ENGINE'] = 'django_postgrespool'
# Adjust according to your database connection limit.
DATABASE_POOL_ARGS = {
    'max_overflow': 15,
    'pool_size': 5,
    'recycle': 300
}
# ######### END DATABASE CONFIGURATION


# #########INTERNATIONALIZATION CONFIGURATION
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# #########END INTERNATIONALIZATION CONFIGURATION


# ######### STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static_deploy')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# See: http://whitenoise.evans.io/en/latest/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# ######### END STATIC FILE CONFIGURATION


# ######### MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/topics/files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Not suitable for production!
MEDIA_URL = '/media/'
# ######### END MEDIA CONFIGURATION


# ######### AUTH CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#auth
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'

# See: https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'accounts.User'

# See: https://docs.djangoproject.com/en/1.8/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    'accounts.backends.AccountBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# See: https://docs.djangoproject.com/en/1.8/topics/auth/passwords/#using-bcrypt-with-django
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
# ######### END AUTH CONFIGURATION


# ########## PYTHON SOCIAL AUTH CONFIGURATION
# Enable social authentication options such as 'Login with Facebook'
# See: http://python-social-auth.readthedocs.org/en/latest/configuration/django.html

INSTALLED_APPS += ('social.apps.django_app.default',)

MIDDLEWARE_CLASSES += ('social.apps.django_app.middleware.SocialAuthExceptionMiddleware',)

# See: http://python-social-auth.readthedocs.org/en/latest/configuration/django.html#autentication-backends
AUTHENTICATION_BACKENDS += (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/login/'
LOGIN_ERROR_URL = '/accounts/login/'

# Allow our users to log in with Facebook, Google, and Twitter.
# Social auth providers require a secret and a key, which should
# be kept out of version control and in environment variables.

# See: http://python-social-auth.readthedocs.org/en/latest/backends/facebook.html
SOCIAL_AUTH_FACEBOOK_KEY = get_env_setting('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = get_env_setting('FACEBOOK_SECRET')
#
# See: http://python-social-auth.readthedocs.org/en/latest/backends/google.html#google-oauth2
# Also be sure to enable the Google+ API to avoid 403 errors.
# Redirect URI should point to http://example.com/complete/google-oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env_setting('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env_setting('GOOGLE_SECRET')

# See: http://python-social-auth.readthedocs.org/en/latest/backends/twitter.html
SOCIAL_AUTH_TWITTER_KEY = get_env_setting('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = get_env_setting('TWITTER_KEY')

# See: http://python-social-auth.readthedocs.org/en/latest/backends/facebook.html
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# See: http://python-social-auth.readthedocs.org/en/latest/pipeline.html
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'accounts.pipeline.request_user_email',
    # 'social.pipeline.mail.mail_validation',
    'accounts.pipeline.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

SOCIAL_AUTH_TWITTER_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'accounts.views.social_auth_validate_email'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/accounts/verification_sent/'
# ########## END PYTHON SOCIAL AUTH CONFIGURATION

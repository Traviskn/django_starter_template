"""
Django development settings for {{cookiecutter.project_name}}.
"""


from .common import *


# ######### SECRET CONFIGURATION
# Set a value for SECRET_KEY as an environment variable for production use.
# The default specified here should only be used for development and testing.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "wnper3(^b)8ud83cshnki#6ql)x$tk6)h=(h@xx2vzksxm-s7y"
# ########## END SECRET CONFIGURATION


# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# See: https://docs.djangoproject.com/en/1.8/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# ######### END DEBUG CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#email-backend
# Emails get printed to the console with this backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ######### END EMAIL CONFIGURATION


# ######### WEBPACK LOADER CONFIGURATION
# See: https://github.com/owais/django-webpack-loader
WEBPACK_LOADER = {
    'BUNDLE_DIR_NAME': 'build/',
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack/webpack-stats.json'),
}
# ######### END WEBPACK LOADER CONFIGURATION

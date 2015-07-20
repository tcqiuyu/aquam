"""
Production settings and globals.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
"""

from __future__ import absolute_import

from os import environ

from .base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

# HOST CONFIGURATION
ALLOWED_HOSTS = [
    "aquam.org",
    "www.aquam.org"
]


# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

EMAIL_PORT = environ.get('EMAIL_PORT', 587)

EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

EMAIL_USE_TLS = True

SERVER_EMAIL = EMAIL_HOST_USER


# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'aquamdb',
        'USER': 'aquam',
        'PASSWORD': 'aquam2015$',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = (
    '/home/aquamuser/webapps/aquam_static/',
)

# CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/aquamuser/memcached.sock',
    }
}


# SECRET CONFIGURATION
SECRET_KEY = get_env_setting('SECRET_KEY')

"""
Django settings for concierge project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'set this to be something secret in production!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# AWS access
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'fair-research-concierge')
AWS_FOLDER = os.getenv('AWS_FOLDER', 'manifests')
AWS_FOLDER_TEST = os.getenv('AWS_FOLDER_TEST', 'manifests-dev')
AWS_STAGING_DIR = os.getenv('AWS_STAGING_DIR', '/tmp/concierge_staging')

# Globus
GLOBUS_DEFAULT_SYNC_LEVEL = 'checksum'

# Bag Settings
BAG_STAGING_DIR = '/tmp/bag_staging'

# Other
SUPPORTED_BAG_PROTOCOLS = ['http', 'https', 'globus']
SUPPORTED_CHECKSUMS = ['md5', 'sha1', 'sha256', 'sha512']
# Shows up as a label on user globus transfer lists
SERVICE_NAME = 'Concierge Service'
with open(os.path.join(BASE_DIR, 'service_description.md')) as f:
    SERVICE_DESCRIPTION = f.read()

CONCIERGE_SCOPE = ('https://auth.globus.org/scopes/'
                   '524361f2-e4a9-4bd0-a3a6-03e365cac8a9/concierge')
TRANSFER_SCOPE = 'urn:globus:auth:scope:transfer.api.globus.org:all'

GLOBUS_KEY = os.getenv('GLOBUS_KEY', '')
GLOBUS_SECRET = os.getenv('GLOBUS_SECRET', '')
SOCIAL_AUTH_GLOBUS_KEY = GLOBUS_KEY
SOCIAL_AUTH_GLOBUS_SECRET = GLOBUS_SECRET
SOCIAL_AUTH_GLOBUS_SCOPE = [CONCIERGE_SCOPE]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_INFO': 'concierge.urls.api',
}


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'social_django',  # django social auth
    'drf_yasg',
    'api',
    'gap',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.auth.GlobusTokenAuthentication',
        'api.auth.GlobusSessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Anonymous users are welcome to the base API
    ],
    'EXCEPTION_HANDLER': 'api.exception_handlers.concierge_exception_handler',
}

AUTHENTICATION_BACKENDS = (
   'social_core.backends.globus.GlobusOpenIdConnect',
   'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/globus/'
LOGOUT_URL = '/logout/'
# Seconds for which a token can be used in-between introspections
GLOBUS_INTROSPECTION_CACHE_EXPIRATION = 30

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'concierge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stream': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'formatters': {
        'simple': {
            'format': '{levelname} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        # Quash invalid host header messages. We get a lot of these from random
        # internet bots connecting via IP. We SHOULD ignore them at the NGINX
        # level, but I'm not sure how to do that with elastic beanstalk yet...
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.db.backends': {
                    'handlers': ['null'],  # Quiet by default!
                    'propagate': False,
                    'level': 'DEBUG',
                    },
        'api': {
            'handlers': ['stream'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'concierge': {
            'handlers': ['stream'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'gap': {
            'handlers': ['stream'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', 'static')

try:
    from concierge.local_settings import *  # NOQA
except ImportError:
    pass

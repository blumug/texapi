# -*- coding: utf-8 -*-
"""Common settings and globals."""


from os.path import abspath, basename, dirname, join, normpath
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

LOCAL_MODE = False
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('en', 'English'),
    ('fr', u'Français'),
)

ALLOWED_LANGUAGES = ('en', 'fr')
DEFAULT_USER_LANGUAGE_CODE = 'en'


########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, '../media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, '../media/static/'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/media/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
)


# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = r"mcx^!5a2jdlw=the)wb!=)ss+816$lkwiy)f6#1a0#kv%d43nu"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'articles.context_processors.root_categories',
    'articles.context_processors.themes',
    'newsletter.context_processors.newsletter',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'reversion.middleware.RevisionMiddleware',
)
########## END MIDDLEWARE CONFIGURATION

########## AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    'core.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
########## END AUTHENTICATION CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',
    'raven.contrib.django.raven_compat',
    'sorl.thumbnail',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'crispy_forms',
    'compressor',
    'bootstrap_pagination',
    'django_extensions',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'core',
    'api_users',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'time_throttled': {
            '()': 'timethrottledfilter.TimeThrottledFilter',
            'quantity': 5,
            'interval': 30,
            'ignore_lines': [],
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 10000,
            'backupCount': 10,
            'filename': join(DJANGO_ROOT, '../logs/texapi.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'sentry', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## CELERY
# See: http://docs.celeryproject.org/en/latest/configuration.html#redis-backend-settings
BROKER_URL = 'redis://localhost/1'
CELERY_RESULT_BACKEND = 'redis://localhost/1'

from kombu import Exchange, Queue

CELERY_DEFAULT_QUEUE = 'texapi'
CELERY_QUEUES = (
    Queue('texapi', Exchange('texapi'), routing_key='texapi'),
)

from celery.schedules import crontab
########## END CELERY


########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'core.exceptions.api_exception_handler',
    'PAGINATE_BY': 10,                 # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
}
########## END REST FRAMEWORK CONFIGURATION



########## REST SWAGGER CONFIGURATION
# See: https://github.com/marcgibbons/django-rest-swagger
SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '1.0',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',  # An API key
    "is_authenticated": True,  # Set to True to enforce user authentication,
    "is_superuser": True,  # Set to True to enforce admin only access
}
########## END REST SWAGGER CONFIGURATION

########### CRISPY FORMS CONFIGURATION
# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html
CRISPY_TEMPLATE_PACK = 'bootstrap3'
########### END CRISPY FORMS CONFIGURATION

########### LOGIN URL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-LOGIN_URL
LOGIN_URL = '/login/'
########### END LOGIN URL CONFIGURATION


########### LOCALE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-LOCALE_PATHS
LOCALE_PATHS = (
    normpath(join(DJANGO_ROOT, '../locale')),
)
########### END LOCALE CONFIGURATION

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

########### DJANGO-COMPRESSOR CONFIGURATION
# See: http://django-compressor.readthedocs.org/en/latest/settings/
COMPRESS_URL = MEDIA_URL
COMPRESS_ROOT = MEDIA_ROOT
COMPRESS_OUTPUT_DIR = 'min'
########### END DJANGO-COMPRESSOR CONFIGURATION

########## EMAIL SETTINGS
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
DEFAULT_FROM_EMAIL = "Notification Textapi <noreply@texapi.fr>"
########## END EMAIL SETTINGS


########## TWITTER CONFIGURATION
TWITTER_APP_CONSUMER_KEY = 'swuPpUyp30qaahEqMUjfA'
TWITTER_APP_CONSUMER_SECRET = 'scvzTnoZVnJRRDdapmecJAvlDYGo2hHjTbBiKxLZF0'
########## END TWITTER CONFIGURATION

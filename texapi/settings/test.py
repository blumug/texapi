from base import *

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
TEST_DISCOVER_TOP_LEVEL = 'apps'
########## SOUTH CONFIGURATION
SOUTH_TESTS_MIGRATE = False
########## END SOUTH CONFIGURATION

INSTALLED_APPS += (
    'django_jenkins',
)
# django-jenkins
PROJECT_APPS = LOCAL_APPS


ES_ENABLED = False

########## CELERY CONFIGURATION
CELERY_ALWAYS_EAGER = True
########## END CELERY CONFIGURATIOn

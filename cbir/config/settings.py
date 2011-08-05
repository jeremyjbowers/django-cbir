import os
'''
Identify the project and its location on the filesystem.
'''
PROJECT_SLUG                = 'django-cbir'
PROJECT_MODULE              = 'cbir'
ROOT_URLCONF                = 'cbir.config.urls'
PROJECT_DIR                 = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
'''
Below is the generic project stuff. This shouldn't change between environments.
'''
TIME_ZONE                   = 'America/New_York'
LANGUAGE_CODE               = 'en-us'
SITE_ID                     = 1
USE_L10N                    = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
)

# GRAPPELLI_INDEX_DASHBOARD = 'blag.config.grappelli.dashboard.CustomIndexDashboard'

INSTALLED_APPS = (
    # 'grappelli.dashboard',
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'sorl.thumbnail',
    'cbir',
)

try:
    from cbir.config.local_settings import *
except ImportError:
    pass

DEBUG                       = True
TEMPLATE_DEBUG              = DEBUG

MEDIA_ROOT                  = os.path.join(PROJECT_DIR, '%s/media' % (PROJECT_SLUG))
MEDIA_URL                   = ''

# GRAPPELLI SETTINGS
ADMIN_MEDIA_PREFIX          = 'http://preps.s3.amazonaws.com/static/grappelli/'

# DJANGO-STORAGES SETTINGS
from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
DEFAULT_FILE_STORAGE        = 'storages.backends.s3.S3Storage'
AWS_STORAGE_BUCKET_NAME     = 'jeremybowerscom'

# SORL-THUMBNAIL SETTINGS

ADMINS = (
     ('Jeremy Bowers', 'jeremyjbowers@gmail.com'),
)
MANAGERS = ADMINS

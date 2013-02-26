# -*- coding: utf-8 -*-
# Django settings for hospinet project.
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

COMPANY = None
if COMPANY != None:
    LOGIN_URL = '/{0}/accounts/signin/'.format(COMPANY)
    LOGOUT_URL = '/{0}/accounts/signout/'.format(COMPANY)
    LOGIN_REDIRECT_URL = '/{0}/accounts/%(username)s/'.format(COMPANY)
#COMPANY = 'hospinet'
else:
    LOGIN_URL = '/accounts/signin/'
    LOGOUT_URL = '/accounts/signout/'
    LOGIN_REDIRECT_URL = '/accounts/%(username)s/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hospinet',                      # Or path to database file if using sqlite3.
        'USER': 'hospinet',                      # Not used with sqlite3.
        'PASSWORD': 'hospinet',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Tegucigalpa'

USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-hn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

if COMPANY != None:
    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = '/{0}/media/'.format(COMPANY)

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/{0}/static/'.format(COMPANY)

    # URL prefix for admin static files -- CSS, JavaScript and images.
    # Make sure to use a trailing slash.
    # Examples: "http://foo.com/static/admin/", "/static/admin/".
    ADMIN_MEDIA_PREFIX = '/{0}/static/admin/'.format(COMPANY)
else:
    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = '/media/'

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/static/'

    # URL prefix for admin static files -- CSS, JavaScript and images.
    # Make sure to use a trailing slash.
    # Examples: "http://foo.com/static/admin/", "/static/admin/".
    ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%d3r*q0fk6#5y-j%88zn#f+pq16)v2x6ap%q_y)7dj+r59@_#^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'hospinet.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.humanize',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # internal apps
    'persona',
    'spital',
    'imaging',
    'users',
    'nightingale',
    'clinique',
    'invoice',
    'emergency',
    # Third party apps go here
    'django_extensions',
    'treemenus',
    'sorl.thumbnail',
    'django_countries',
    'haystack',
    'tastypie',
    'actstream',
    'south',
    'private_files',
    'userena',
    'guardian',
    'easy_thumbnails',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

AUTH_PROFILE_MODULE = 'users.Profile'

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_PATH,'whoosh_index'),
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}
# Additional Settings
FILE_PROTECTION_METHOD = 'basic'
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'users.UserProfile'
USE_THOUSAND_SEPARATOR = True
LANGUAGE_CODE = 'es-NI'
TIME_ZONE = 'America/Tegucigalpa'

ACTSTREAM_ACTION_MODELS = (
    'auth.user',
    'auth.group',
    'nightingale.SignoVital',
    'nightingale.Evolución',
    'nightingale.Cargo',
    'nightingale.OrdenMedica',
    'nightingale.Ingesta',
    'nightingale.Excreta',
    'nightingale.NotaEnfermeria',
    'nightingale.Glicemia',
    'nightingale.Glucosuria',
    'nightingale.Insulina',
    'nightingale.Sumario',
    'nightingale.Medicamento',
    'nightingale.Dosis',
    'nightingale.Evolucion',
    'invoide.Recibo',
    'spital.Admision',
    'comments.comment')

ACTSTREAM_MANAGER = 'actstream.managers.ActionManager'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'me@gmail.com'
#EMAIL_HOST_PASSWORD = 'password'

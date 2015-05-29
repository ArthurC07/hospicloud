# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

# Django settings for hospinet project.
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


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

DEBUG = env_var('DEBUG', True)
TEMPLATE_DEBUG = env_var('DEBUG', True)

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env_var('DBNAME', 'hospinet'),
        # Or path to database file if using sqlite3.
        'USER': env_var('DBUSER', 'hospinet'), # Not used with sqlite3.
        'PASSWORD': env_var('DBPASSWORD', 'hospinet'), # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

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
LANGUAGE_CODE = 'es-MX'

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
    os.path.join(PROJECT_PATH, '../templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
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
    'inventory',
    'statistics',
    'contracts',
    'lab',
    # Third party apps go here
    'django_extensions',
    'django_countries',
    'tastypie',
    'userena',
    'guardian',
    'easy_thumbnails',
    'crispy_forms',
    'bootstrap_pagination',
    'select2',
    'constance',
    'constance.backends.database',
    'csvimport.app.CSVImportConf',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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
    'django.contrib.messages.context_processors.messages',
    'hospinet.context_processors.chat'
)

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
# Additional Settings
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'users.UserProfile'
USE_THOUSAND_SEPARATOR = True
USERENA_ACTIVATION_REQUIRED = False

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'RTN': (u'', u'Registro Tributario Nacional'),
    'RECEIPT_ROOT': (u'PlaceHolder', u'Prefijo para recibos'),
    'COMPANY_NAME': (u'COMPANY_NAME', u'Nombre de la Empresa'),
    'COMPANY_ADDRESS': (u'', u'Dirección de la Compañía'),
    'EMERGENCIA': (1, u'Cuenta utilizada para estadia en emergencias'),
    'INVOICE_OFFSET': (0, u'Numeración para iniciar recibos'),
    'DEPOSIT_ACCOUNT': (1, u'Cuenta utilizada para disminuir depositos'),
    'EXTRA_EMERGENCIA': (1, u'Cuenta utilizada para agregar tiempo extra de emergencias'),
    'DEPOSIT_PAYMENT': (1, u'Tipo de Pago para Abonos a cuenta'),
    'CHAT': (u'http://www.example.com', u'Url para el chat interno'),
    'ONLINE_HELP': (u'http://www.example.com', u'Url para ayuda en línea'),
    'SYSTEM_EMAIL': (u'me@localhost', u'Email utilizado para enviar correo'),
    'NOTIFICATION_EMAIL': (u'me@localhost', u'Email para notificar'),
    'DEFAULT_VENTA_TYPE': (1, u'Tipo de Venta Predeterminada'),
    'DEFAULT_CONSULTA_ITEM': (1, u'Costo de Consulta'),
    'NIGHT_CONSULTA_ITEM': (1, u'Costo de Consulta Nocturna'),
    'ELDER_VENTA_TYPE': (1, u'Tipo de Venta Predeterminada'),
    'ELDER_AGE': (60, u'Edad mínima de la Tercera Edad'),
    'CONSULTA_ENABLED': (1, u'Consulta habilitada'),
    'EMERGENCIA_ENABLED': (1, u'Emergencia Habilitada'),
    'HOSPITALIZACION_ENABLED': (1, u'Hospitalizacion Habilitada'),
    'IMAGENES_ENABLED': (1, u'Imagenes Habilitadas'),
    'CONTRATOS_ENABLED': (1, u'Edad mínima de la Tercera Edad'),
    'DEFAULT_CLIENT': (1, u'Cliente Predeterminado para los recibos'),
    'RECEIPT_DAYS': (1, u'Dias que dura una factura al credito'),
}


#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'me@gmail.com'
#EMAIL_HOST_PASSWORD = 'password'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
WSGI_APPLICATION = 'hospinet.wsgi.application'

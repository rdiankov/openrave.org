# -*- coding: utf-8 -*-
# Copyright (C) 2012 Rosen Diankov <rosen.diankov@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Settings for www.openrave.org

import os, json
ROOT_PATH = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    OPENRAVEORG_ENV = os.environ['OPENRAVEORG_ENV'].lower()
except KeyError:
    OPENRAVEORG_ENV = 'dev'

# It's a secret to everybody
if OPENRAVEORG_ENV=='production':
    SECRETS = json.load(open('/var/openrave.org_secrets.json'))
else:
    SECRETS = json.load(open(os.path.join(ROOT_PATH,'..','openrave.org_secrets.json')))
    
SECRET_KEY = str(SECRETS['secret_key'])
# SUPERFEEDR_CREDS is a 2 element list in the form of [email,secretkey]
SUPERFEEDR_CREDS = SECRETS.get('superfeedr_creds')

ADMINS = ( ('OpenRAVE Development', 'openrave.testing@gmail.com'), ('Rosen Diankov', 'rosen.diankov@gmail.com') )
MANAGERS = ADMINS
FEED_APPROVERS_GROUP_NAME = "feed-approver"

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openrave_website',
        'USER': 'openrave',
        'PASSWORD': 'testpass',
        'HOST': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS=( os.path.join(ROOT_PATH,'..','locale'), )

IPYTHON_DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = "noreply@openrave.org"

MEDIA_ROOT = os.path.join(ROOT_PATH,'..','media/')
MEDIA_URL = '/m/'

STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/s/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH,'static'),
    os.path.join(ROOT_PATH,'static'+OPENRAVEORG_ENV),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ALLOWED_HOSTS = []

# Application definition
WSGI_APPLICATION = 'openrave_org.wsgi.application'
SITE_ID = 1
ROOT_URLCONF = 'openrave_org.urls'
INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django_push.subscriber',
    'haystack',
    'openrave_org.docs',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

# note that doxygen search will not work so have to exempt this
X_FRAME_OPTIONS = 'DENY'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += ('openrave_org.docs.context_processors.recent_release',)


# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 3

# comment_utils settings
#AKISMET_API_KEY = "?"

# setting for documentation root path
OPENRAVE_DOCUMENT_ROOT_PATH = os.path.join(ROOT_PATH,'..','docdata')

# Haystack settings
#HAYSTACK_SITECONF = 'openrave_website.docs.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'whoosh'
#HAYSTACK_WHOOSH_PATH = os.path.join(OPENRAVE_DOCUMENT_ROOT_PATH,'openravedocs.index')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(OPENRAVE_DOCUMENT_ROOT_PATH,'openravedocs.index'),
    }
}
if OPENRAVEORG_ENV=='production':
    from settings_production import *

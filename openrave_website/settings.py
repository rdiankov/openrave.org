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

import os
import json
import platform

ROOT_PATH = os.path.dirname(__file__)

try:
    OPENRAVEORG_ENV = os.environ['OPENRAVEORG_ENV'].lower()
except KeyError:
    OPENRAVEORG_ENV = 'dev'

# It's a secret to everybody
SECRETS = json.load(open(os.path.join(ROOT_PATH,'..','openrave.org_secrets.json')))
SECRET_KEY = str(SECRETS['secret_key'])
# SUPERFEEDR_CREDS is a 2 element list in the form of [email,secretkey]
SUPERFEEDR_CREDS = SECRETS.get('superfeedr_creds')

ADMINS = ( ('Rosen Diankov', 'rosen.diankov@gmail.com'), )
MANAGERS = ADMINS
FEED_APPROVERS_GROUP_NAME = "feed-approver"
TIME_ZONE = 'UTC'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openrave_website',
        'USER': 'openrave',
        'PASSWORD': 'testpass',
        'HOST': 'localhost',
        'PORT': '5432',
        'TIME_ZONE': 'UTC',
        }
    }
}

# djangoproject.com has a router for Trac (django_website.trac.db_router.TracRouter) that can create django models from trac tables
DATABASE_ROUTERS = []

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS=(
    os.path.join(ROOT_PATH,'..','locale'),
    )

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates'),
)
MEDIA_ROOT = ''

DEBUG = True
PREPEND_WWW = False
CACHE_BACKEND = "dummy:///"
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/admin_media/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1
ROOT_URLCONF = 'openrave_website.urls'
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django_push.subscriber',
    'openrave_website',
    'registration',
    'south',
    'djangosecure',
    'haystack'
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'openrave'
CACHE_MIDDLEWARE_GZIP = True
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

MIDDLEWARE_CLASSES = [
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "openrave_website.context_processors.recent_release",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    ]

DEFAULT_FROM_EMAIL = "noreply@openrave.org"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {"format": "[%(name)s] %(levelname)s: %(message)s"},
        "full": {"format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"}
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django_website": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    }
}

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 3

# comment_utils settings
#AKISMET_API_KEY = "?"

# setting for documentation root path
OPENRAVE_DOCUMENT_ROOT_PATH = os.path.join(ROOT_PATH,'docs')

# Haystack settings
HAYSTACK_SITECONF = 'openrave_website.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(OPENRAVE_DOCUMENT_ROOT_PATH,'openravedocs.index')

# PubSubHubbub settings
#PUSH_HUB = 'https://superfeedr.com/hubbub'
#PUSH_CREDENTIALS = 'django_website.aggregator.utils.push_credentials'
#PUSH_SSL_CALLBACK = False

# If django-debug-toolbar is installed enable it.
# if DEBUG:
#     try:
#         import debug_toolbar
#     except ImportError:
#         pass
#     else:
#         # Insert DDT after the common middleware
#         common_index = MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware')
#         MIDDLEWARE_CLASSES.insert(common_index+1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
#         INTERNAL_IPS = ['127.0.0.1']
#         INSTALLED_APPS.append('debug_toolbar')

# Log errors to Sentry instead of email, if available.
if 'sentry_dsn' in SECRETS:
    INSTALLED_APPS.append('raven.contrib.django')
    #example SENTRY_DSN = 'http://public_key:secret_key@example.com/1'
    SENTRY_DSN = SECRETS['sentry_dsn']
    LOGGING["loggers"]["django.request"]["handlers"].remove("mail_admins")

# This has yet to be configured for TOB use

from os.path import join, normpath

from base import *


########## DEBUG CONFIG
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIG


########## EMAIL CONFIG
## Uncomment following to enable email testing locally
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = "localhost"
# EMAIL_PORT = 1025

# or,
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIG


########## DATABASE CONFIG
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIG


########## CACHE CONFIG
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIG


########## TOOLBAR CONFIG
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}
########## END TOOLBAR CONFIG


######### EVENT CONFIG
# Eventbrite credentials
# Event_id needs to be configured per event//find the ID on eventbrite
# Generate/copy keys from Eventbrite account
## DON'T PUSH KEYS TO PUBLIC REPOS!!!
EVENTBRITE = ''
EB_EVENT_ID = ''
EB_APP_KEY = ''
EB_USER_KEY = ''

# Contact info for current event; for email templates
EVENT_NAME = 'SymposionCon' ## Change if creating custom event test site
EVENT_WEBSITE = ''
EVENT_EMAIL = '' # eg, info@djangocon.us
EVENT_PHONE = '' # eg, our contact phone
########## END EVENT CONFIGS
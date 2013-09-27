# Configured for TOB use

from base import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"

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

# Eventbrite credentials
# Event_id needs to be configured per event//find the ID on eventbrite
# Generate/copy keys from Eventbrite account
## DON'T PUSH KEYS TO PUBLIC REPOS!!!
EVENTBRITE = ''
EB_EVENT_ID = ''
EB_APP_KEY = ''
EB_USER_KEY = ''

# Contact info for current event; for email templates
EVENT_NAME = ''
EVENT_WEBSITE = ''
EVENT_EMAIL = '' # eg, info@djangocon.us
EVENT_PHONE = '' # eg, our contact phone

import os.path
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Include apps on the path
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

# People who get code error notifications when DEBUG=False
ADMINS = (('Your admin name', 'admin@example.com'),)

#AUTH_PROFILE_MODULE = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'krater_development',
    }
}

# Never deploy a site into production with DEBUG turned on!
DEBUG = True

# Address to use for various automated correspondence from the site manager(s).
DEFAULT_FROM_EMAIL = 'webmaster@example.com'

# Maximum size (in bytes) before an upload gets streamed to the file system.
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# List of locations of the fixture data files, in search order
FIXTURE_DIRS = ()

# A tuple of strings designating all the enabled applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'mongonaut',
    'social_auth',
    'tastypie',

    'krater',
)

# The language code for this installation
LANGUAGE_CODE = 'en-us'

# Who should get broken-link notifications when SEND_BROKEN_LINK_EMAILS=True
MANAGERS = ADMINS

# Absolute path to the directory that holds stored files.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'uploads')

# URL that handles the media served from MEDIA_ROOT (must end in a slash)
MEDIA_URL = '/uploads/'

# A tuple of middleware classes to use
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Number of digits grouped together on the integer part of a number
NUMBER_GROUPING = 3

# The full Python import path to the root URLconf
ROOT_URLCONF = 'urls'

# Seed for secret-key hashing algorithms
SECRET_KEY = '6cc3bf11675ef9b2d7b45d61f444c1decbf1bbf3d2a1b585e5'

# The ID of the current site in the django_site database table
#SITE_ID = u'4f29d161213ca38657000021'
SITE_ID = u'4f2f25a4cb4a055317000021'

# Absolute path to the directory where collectstatic will collect static files
STATIC_ROOT = ''

# Additional locations the staticfiles app will traverse
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# URL prefix for CSS, JavaScript and images used by the Django admin.
# Use a trailing slash, and to have this be different from MEDIA_URL
# For integration with staticfiles, this should be  STATIC_URL + 'admin/'.
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'social_auth.context_processors.social_auth_by_name_backends',
    #'social_auth.context_processors.social_auth_backends', # Do not use with social_auth_by_type_backends
    'social_auth.context_processors.social_auth_by_type_backends', # Do not use with social_auth_backends
)

# Display a detailed report for any TemplateSyntaxError.
TEMPLATE_DEBUG = DEBUG

# List of locations of the template source files, in search order
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# A tuple of template loader classes, specified as strings
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# The time zone for this installation
TIME_ZONE = 'America/Los_Angeles'

# Output the "Etag" header. This saves bandwidth but slows down performance
USE_ETAGS = False

# Display numbers using a thousand separator
USE_THOUSAND_SEPARATOR = True

# Enable Django's internationalization system
USE_I18N = False

# Display numbers and dates using the format of the current locale
USE_L10N = False

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'mongoengine.django.auth.MongoEngineBackend',
)
SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'google-oauth', 'facebook', 'twitter')

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
GOOGLE_CONSUMER_KEY = ''
GOOGLE_CONSUMER_SECRET = ''
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

LOGIN_URL = '/login-form/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL = '/login-error/'

SESSION_ENGINE = 'mongoengine.django.sessions'

# mongodb connection
from mongoengine import connect
connect('krater_development')

MONGONAUT_JQUERY = "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
MONGONAUT_TWITTER_BOOTSTRAP = "http://twitter.github.com/bootstrap/assets/css/bootstrap.css"
MONGONAUT_TWITTER_BOOTSTRAP_ALERT = "http://twitter.github.com/bootstrap/assets/js/bootstrap-alert.js"

# Import local settings
try:
    from settings.local_settings import *
except ImportError:
    print 'Unable to import local_settings.py. Skipped.'

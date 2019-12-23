"""
Django settings for website on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# BASE_DIR = /path/to/app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PROJECT_ROOT = /path/to/app/website
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def bool_environ(name):
    if name in os.environ:
        return os.environ[name].lower() == 'true'
    return False

def str_environ(name, default=None):
    if name in os.environ:
        return os.environ[name]
    return default

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "2hp_c&e=@jq4l*_x64n26!8w&h)7*cc-qe4q#0(+as7x6c+n1#"

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = bool_environ('PRODUCTION')
DEBUG = bool_environ('DEBUG')

# TODO: set to False when emails are working
AUTO_ACTIVATE_ACCOUNTS = True

FROM_EMAIL = str_environ("FROM_EMAIL")
BCC_EMAIL = str_environ("BCC_EMAIL")
REPLY_TO_EMAIL = str_environ("REPLY_TO_EMAIL")

# The URL for the sponsorship packet, to download if SPONSORSHIP_PACKET_FILE
# does not exist in the filesystem.
SPONSORSHIP_PACKET_URL = str_environ("SPONSORSHIP_PACKET_URL")

# The local name of the sponsorship packet, to be stored in the website/static
# folder. If this file exists, it will be used. Otherwise, it will be
# redownloaded from SPONSORSHIP_PACKET_URL.
SPONSORSHIP_PACKET_FILE = str_environ("SPONSORSHIP_PACKET_FILE", "sponsorship.pdf")

if not PRODUCTION and 'DEBUG' not in os.environ:
    DEBUG = True

if PRODUCTION:
    REGISTRATION_TOKEN = os.environ['REGISTRATION_TOKEN']
    SECRET_KEY = os.environ['SECRET_KEY']
    if not bool_environ('ALLOW_HTTP'):
        SECURE_SSL_REDIRECT = True
elif DEBUG:
    # Disables token requirement
    REGISTRATION_TOKEN = None

# Application definition

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    ####################
    ### Dependencies ###
    ####################
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django_extensions",
    "debug_toolbar",
    # HTML
    "django_jinja",
    "widget_tweaks",
    "ckeditor",
    # Models
    "phonenumber_field",
    ####################
    ### Project Apps ###
    ####################
    "shared",
    "profiles",
    "companies",
    "contacts",
    "dashboard",
    "emails",
    "hackathons",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shared.middleware.CurrentHackathonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shared.contextprocessors.fill_current_hackathon_as_h",
            ],
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',
                'django.contrib.humanize.templatetags.humanize',
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_USER_MODEL = "profiles.User"
LOGIN_URL = "/login"
LOGOUT_REDIRECT_URL = "/login"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = "America/New_York"

# Phonenumber Formatting
PHONENUMBER_DEFAULT_REGION = "US"
PHONENUMBER_DB_FORMAT = "NATIONAL"

# Change 'default' database configuration with $DATABASE_URL.
DATABASES["default"].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers
ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_STORAGE = 'shared.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())

# Email thing
if 'SENDGRID_API_KEY' in os.environ:
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
elif 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    EMAIL_BACKEND = 'django_ses.SESBackend'
else:
    print("WARNING: No email backend configured.")
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "TODO: email host"
# EMAIL_HOST_USER = "TODO: email host user"
# EMAIL_HOST_PASSWORD = "TODO: email host password"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
    },
    'basic_fill': {
        'toolbar': 'Basic',
        'width': '100%',
    },
}

def is_debug(self):
    return DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': is_debug,
    'DISABLE_PANELS': (
        # Enabled by default:
        # 'debug_toolbar.panels.versions.VersionsPanel',
        # 'debug_toolbar.panels.timer.TimerPanel',
        # 'debug_toolbar.panels.settings.SettingsPanel',
        # 'debug_toolbar.panels.headers.HeadersPanel',
        # 'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ),
    'SHOW_COLLAPSED': True,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

try:
    from .settings_secret import *
except ImportError:
    pass

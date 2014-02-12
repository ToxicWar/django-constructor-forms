# coding: utf-8
import os

VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
MEDIA_ROOT = os.path.join(VIRTUAL_ENV, 'www', 'media')
STATIC_ROOT = os.path.join(VIRTUAL_ENV, 'www', 'static')
SITE_ID = 1
ANONYMOUS_USER_ID = -1
USE_TZ=True
SECRET_KEY = 'hey hey hey'
ROOT_URLCONF = 'constructor_forms.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'constructor_forms',
    'constructor_forms.tests.test_app',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
coverage_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

CONSTRUCTOR_FORMS_MODIFICATION_WIDGETS = {}

CONSTRUCTOR_FORMS_EXTRA_FIELDS = []

NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-package=constructor_forms',
    '--cover-html',
    '--cover-html-dir=%s' % coverage_dir,
    '--cover-inclusive',
    '--rednose',
    '--nologcapture',
    #'-x'
]

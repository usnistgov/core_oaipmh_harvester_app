from os.path import dirname, realpath

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    # Local apps
    "tests",
]

OAI_HARVESTER_ROOT = dirname(realpath(__file__))

SSL_CERTIFICATES_DIR = 'certs'

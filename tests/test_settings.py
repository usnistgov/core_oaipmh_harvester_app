from os.path import dirname, realpath

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
    'django.contrib.auth',
    'django.contrib.contenttypes',
]
OAI_HARVESTER_ROOT = dirname(realpath(__file__))
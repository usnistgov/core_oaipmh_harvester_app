from os.path import dirname, realpath

from core_main_app.utils.databases.mongoengine_database import Database

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    # Local apps
    "core_main_app",
    "tests",
]

OAI_HARVESTER_ROOT = dirname(realpath(__file__))

SSL_CERTIFICATES_DIR = 'certs'

MOCK_DATABASE_NAME = 'db_mock'
MOCK_DATABASE_HOST = 'mongomock://localhost'

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()

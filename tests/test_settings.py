from os.path import dirname, realpath

from core_main_app.utils.databases.mongoengine_database import Database

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Local apps
    "core_main_app",
    "tests",
]

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]


OAI_HARVESTER_ROOT = dirname(realpath(__file__))

SSL_CERTIFICATES_DIR = True
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

MOCK_DATABASE_NAME = "db_mock"
MOCK_DATABASE_HOST = "mongomock://localhost"

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()

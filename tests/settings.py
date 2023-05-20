
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "atms.apps.AtmsConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "artemis",
        "USER": "postgres",
        "PASSWORD": "admin",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

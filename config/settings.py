from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Development settings, unsuitable for production: a placeholder key and DEBUG on.
SECRET_KEY = "django-insecure-vyk%9n-62-96tt)iu8m^ib3!-1-lqnh2gmcjiopo@_sx)5810%"
DEBUG = True

INSTALLED_APPS = [
    "django.contrib.staticfiles",  # the browsable API's CSS and JS
    "rest_framework",
    "shipments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

# Needed only for the browsable API's HTML pages.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# No authentication by design: every endpoint is open (see the README).
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
}

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
Django settings for blango project.

"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key  
from dotenv import load_dotenv
import django_stubs_ext
from configurations import Configuration, values


django_stubs_ext.monkeypatch()
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

class Base(Configuration):
    SECRET_KEY = get_random_secret_key()
    DEBUG = False
    TEST_DATABASE_PREFIX = 'test'
    ALLOWED_HOSTS = ["*"]
    MIDDLEWARE = [
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]
    #SECTION -  Application definition

    INSTALLED_APPS = [
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "blog",
        "crispy_forms",
        "crispy_bootstrap5",
        "django.contrib.humanize"

    ]
    CRISPY_TEMPLATE_PACK = "bootstrap5"
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    ROOT_URLCONF = "blango.urls"
    TEMPLATE_DIRS = [BASE_DIR / "templates"]
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": TEMPLATE_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "blango.wsgi.application"
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ],
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = "/static/"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    }
}

class Dev(Base):
    DEBUG = True
       # Database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "PORT": 6767,
            "HOST": "localhost",
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "USER": os.getenv("POSTGRES_USER")
        }
    }
    PASSWORD_HASHERS = [
      'django.contrib.auth.hashers.Argon2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
      'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
  ]



class Prod(Dev):
    DEBUG = True

    LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

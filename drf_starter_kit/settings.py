"""
Django settings for drf_starter_kit project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import environ
import os


APP_LABEL = "DRF Starter Kit"


root = environ.Path(__file__) - 2  # Set location 2 folders back (/a/b/ - 2 => /)
DEFAULT_ENV_PATH = root()  # Default location of .env file
DEFAULT_ENV_FILE = os.path.join(DEFAULT_ENV_PATH, ".env")


env = environ.Env(
    SERVER_ENV=(str, "local"),
    DJANGO_DEBUG=(bool, False),
    SECRET_KEY=(str, "some-insecure-key"),
    DB_NAME=(str, "<NOT_SET>"),
    DB_USER=(str, "<NOT_SET>"),
    DB_PASS=(str, "<NOT_SET>"),
    DB_HOST=(str, "localhost"),
    DB_PORT=(str, "5432"),
)
environ.Env.read_env(env.str("ENV_PATH", DEFAULT_ENV_FILE))  # Reading .env file
ENV_VARS = env


ENV = env("SERVER_ENV")  # Environment we're running on, e.g. "local", "test", "prod"
DEBUG = env("DJANGO_DEBUG")  # SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = env("SECRET_KEY")  # SECURITY WARNING: keep the secret key used in production secret!


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# TODO: Change it before going to prod
ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    # Standard Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Our apps
    "foundation",
    # Third party apps
    "rest_framework",
    "corsheaders",
    "django_linear_migrations",
    "drf_yasg",
]


MIDDLEWARE = [
    # Default Django provided middlewares
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Manually added middlewares
    "corsheaders.middleware.CorsMiddleware",
]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    # "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


ROOT_URLCONF = "drf_starter_kit.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


WSGI_APPLICATION = "drf_starter_kit.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASS"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


AUTH_USER_MODEL = "foundation.User"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/"
# STATIC_ROOT = "/app/staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWS_CREDENTIALS = True
# TODO: Configure before deployment
# CORS_URLS_REGEX = r"^/(api|admin)/.*$"

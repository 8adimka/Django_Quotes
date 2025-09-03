import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_SECRET_KEY=(str, "dev-secret-change-me"),
    DJANGO_ALLOWED_HOSTS=(str, "*"),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
    CSRF_TRUSTED_ORIGINS=(str, ""),
    TIME_ZONE=(str, "Europe/Madrid"),
    WEIGHT_LIKE_STEP=(float, 0.2),
    WEIGHT_DISLIKE_STEP=(float, 0.1),
    MIN_EFFECTIVE_WEIGHT=(float, 0.05),
)

# read .env if exists
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=False)

DEBUG = env("DJANGO_DEBUG")
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in env("CSRF_TRUSTED_ORIGINS").split(",") if o.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "quotes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "quotes" / "templates"
        ],  # app templates already inside; kept for clarity
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db(),  # parses DATABASE_URL
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_TZ = True  # keep True for DB consistency

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "quotes" / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Weight logic params
WEIGHT_LIKE_STEP = env("WEIGHT_LIKE_STEP")  # + per like
WEIGHT_DISLIKE_STEP = env("WEIGHT_DISLIKE_STEP")  # - per dislike
MIN_EFFECTIVE_WEIGHT = env("MIN_EFFECTIVE_WEIGHT")  # lower bound to keep chance > 0

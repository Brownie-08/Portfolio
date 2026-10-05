"""
Production settings for PythonAnywhere deployment.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *


DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=env.list("ALLOWED_HOSTS", default=[]),
)
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "Set DJANGO_ALLOWED_HOSTS or ALLOWED_HOSTS for production "
        "(for example: yourusername.pythonanywhere.com)."
    )

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

if SECRET_KEY == "django-insecure-development-only-change-me":
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY or SECRET_KEY for production.")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "portfolio-cache",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"

if "debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS.remove("debug_toolbar")

MIDDLEWARE = [middleware for middleware in MIDDLEWARE if "debug_toolbar" not in middleware]

os.makedirs(MEDIA_ROOT, exist_ok=True)

STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

"""
Development settings for portfolio_project.

This file contains settings specific to development environment.
Inherits from base.py and overrides/adds development-specific configurations.
"""

from .base import *
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed hosts for development
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0', cast=Csv())

# Database configuration for development
# Using environment variables with SQLite as fallback
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # If DATABASE_URL is provided, use dj-database-url to parse it
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL)
        }
    except ImportError:
        # Fallback to SQLite if dj-database-url is not available
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    # Default SQLite configuration for development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Development-specific apps
if DEBUG:
    # Add django_extensions if available
    try:
        import django_extensions
        INSTALLED_APPS += ["django_extensions"]
    except ImportError:
        pass
    
    # Add debug toolbar if available
    try:
        import debug_toolbar
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
        
        # Debug toolbar configuration
        INTERNAL_IPS = [
            "127.0.0.1",
            "localhost",
        ]
        
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG and request.META.get('REMOTE_ADDR') in INTERNAL_IPS,
        }
    except ImportError:
        pass

# Email backend for development (console output)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'portfolio': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Development-specific security settings (less restrictive)
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

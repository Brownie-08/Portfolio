"""
Vercel-specific settings for portfolio_project.

This file contains settings optimized for Vercel deployment.
"""

from .production import *
import os

# Vercel-specific overrides
DEBUG = False

# Vercel provides domain automatically
ALLOWED_HOSTS = ['*']  # Vercel handles this securely

# Database - SQLite only for Vercel serverless
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',  # Vercel temp directory
    }
}

# Static files for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Media files for Vercel
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Disable some security features that might cause issues on Vercel
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

# Logging for Vercel
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Vercel timeout settings
WSGI_APPLICATION = 'portfolio_project.wsgi.application'

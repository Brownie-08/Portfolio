"""
Production settings for portfolio_project.

This file contains settings specific to production environment.
Inherits from base.py and overrides/adds production-specific configurations.
Includes security hardening and performance optimizations.
"""

from .base import *
from decouple import config, Csv
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for production - must be configured via environment variables
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Ensure ALLOWED_HOSTS is properly configured in production
if not ALLOWED_HOSTS and not DEBUG:
    raise ValueError("ALLOWED_HOSTS must be configured in production environment")

# Database configuration for production
# Expects DATABASE_URL environment variable
DATABASE_URL = config('DATABASE_URL')

try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
except ImportError:
    raise ImportError("dj-database-url is required for production database configuration")

# Email configuration for production
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Security Settings for Production
# HTTPS and Security Headers
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# Cookie Security
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Strict')
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=3600, cast=int)  # 1 hour

CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', default='Strict')

# Content Security and Headers
SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY', default='strict-origin-when-cross-origin')
SECURE_CROSS_ORIGIN_OPENER_POLICY = config('SECURE_CROSS_ORIGIN_OPENER_POLICY', default='same-origin')

# Additional Security Settings
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Proxy Settings (for deployment behind reverse proxy)
USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', default=True, cast=bool)
USE_X_FORWARDED_PORT = config('USE_X_FORWARDED_PORT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Performance Settings
# Cache configuration
CACHE_TTL = config('CACHE_TTL', default=300, cast=int)  # 5 minutes default
CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': config('CACHE_LOCATION', default=''),
        'TIMEOUT': CACHE_TTL,
        'OPTIONS': {
            'MAX_ENTRIES': config('CACHE_MAX_ENTRIES', default=1000, cast=int),
        }
    }
}

# Session Configuration
SESSION_ENGINE = config('SESSION_ENGINE', default='django.contrib.sessions.backends.cached_db')
SESSION_CACHE_ALIAS = 'default'

# Static and Media Files for Production
# WhiteNoise is already configured in base.py
WHITENOISE_USE_FINDERS = config('WHITENOISE_USE_FINDERS', default=False, cast=bool)
WHITENOISE_AUTOREFRESH = config('WHITENOISE_AUTOREFRESH', default=False, cast=bool)

# Media files - consider using cloud storage in production
# Configure these if using cloud storage like AWS S3
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='')

if AWS_STORAGE_BUCKET_NAME:
    # Use S3 for media files if configured
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Logging Configuration for Production
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
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': config('LOG_FILE_PATH', default='/var/log/django/portfolio.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        }
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': config('DJANGO_LOG_LEVEL', default='WARNING'),
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'portfolio': {
            'handlers': ['file', 'console'],
            'level': config('APP_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}

# Admin Configuration
ADMINS = [
    (config('ADMIN_NAME', default='Admin'), config('ADMIN_EMAIL', default='admin@example.com')),
]
MANAGERS = ADMINS

# Server Email for error notifications
SERVER_EMAIL = config('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Data Upload Settings
DATA_UPLOAD_MAX_MEMORY_SIZE = config('DATA_UPLOAD_MAX_MEMORY_SIZE', default=5242880, cast=int)  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', default=5242880, cast=int)  # 5MB

# Rate Limiting and Security
# These would require additional packages like django-ratelimit or django-axes
# RATELIMIT_ENABLE = True
# AXES_ENABLED = True

# Monitoring and Health Checks
HEALTH_CHECK_URL = config('HEALTH_CHECK_URL', default='/health/')

# Force HTTPS in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

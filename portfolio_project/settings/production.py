"""
Production settings for portfolio_project.

This file contains settings specific to production environment.
Inherits from base.py and overrides/adds production-specific configurations.
"""

from .base import *
from decouple import config, Csv
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for production - Render and custom domains
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# Add Render domain if provided
render_domain = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if render_domain:
    ALLOWED_HOSTS.append(render_domain)

# Ensure localhost and common domains are allowed
if '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '.onrender.com'])

# Database configuration for production
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Use DATABASE_URL for production (PostgreSQL preferred)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    
    # Add PostgreSQL-specific options for better performance
    if 'postgres' in DATABASE_URL or 'postgresql' in DATABASE_URL:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        DATABASES['default']['CONN_MAX_AGE'] = 600
        
    # Add MySQL options if it's a MySQL database (fallback)
    elif 'mysql' in DATABASE_URL:
        DATABASES['default']['OPTIONS'] = {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
else:
    # Fallback to SQLite for local development only
    import os
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Email backend for production
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# Production-specific security settings
# Render.com SSL configuration
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
# Secure cookies for Render (Render provides proper HTTPS)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Content Security Policy (if django-csp is used)
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net")
# CSP_SCRIPT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net")
# CSP_IMG_SRC = ("'self'", "data:", "https:")

# Logging configuration for production (Railway - console only)
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
            'level': 'INFO',
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
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration for production (optional)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
} if config('REDIS_URL', default=None) else {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db' if config('REDIS_URL', default=None) else 'django.contrib.sessions.backends.db'


# Disable debug toolbar in production
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

# Remove debug middleware
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'debug_toolbar' not in middleware]

# Media files configuration for Cloudinary
if config('USE_CLOUDINARY', default=False, cast=bool):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': config('CLOUDINARY_API_KEY'),
        'API_SECRET': config('CLOUDINARY_API_SECRET')
    }
    MEDIA_URL = 'https://res.cloudinary.com/' + config('CLOUDINARY_CLOUD_NAME') + '/image/upload/'
else:
    import os
    # Use default Django file storage for media files
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Media files settings
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    # Ensure media directory exists
    os.makedirs(MEDIA_ROOT, exist_ok=True)

# Keep STATICFILES_STORAGE pointed at WhiteNoise for static assets
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

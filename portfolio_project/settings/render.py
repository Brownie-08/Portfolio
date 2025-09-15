"""
Render.com production settings for portfolio_project.

This file contains settings specific to Render deployment.
Inherits from base.py and adds Render-specific configurations.
"""

from .base import *
import dj_database_url
import os
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for Render - including .onrender.com domains
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Add Render's external hostname if provided
render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)

# Ensure Render domains are allowed
if not any('.onrender.com' in host for host in ALLOWED_HOSTS):
    ALLOWED_HOSTS.extend(['.onrender.com'])

# If no hosts specified or wildcard, use secure defaults
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# Database configuration - Render provides DATABASE_URL automatically
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    
    # PostgreSQL-specific options for better performance on Render
    if 'postgres' in DATABASE_URL:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        DATABASES['default']['CONN_MAX_AGE'] = 600
        # Enable connection pooling
        DATABASES['default']['CONN_HEALTH_CHECKS'] = True
else:
    # Fallback - should not be used in production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Security settings for HTTPS (Render provides SSL automatically)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# Cookie security
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# CSRF trusted origins for Render
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

# Add custom domain if provided
custom_domain = config('CUSTOM_DOMAIN', default=None)
if custom_domain:
    CSRF_TRUSTED_ORIGINS.append(f'https://{custom_domain}')
    ALLOWED_HOSTS.append(custom_domain)

# Static files configuration for Render
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Additional WhiteNoise settings for better performance
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = False  # Disable in production for performance
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br']

# Logging configuration for Render
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
        'level': 'WARNING',
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

# Email configuration for production
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# Cache configuration - Use Redis if available on Render
redis_url = config('REDIS_URL', default=None)
if redis_url:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': redis_url,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'portfolio',
            'TIMEOUT': 300,
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_CACHE_ALIAS = 'default'
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Remove debug toolbar in production
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

# Remove debug toolbar middleware
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'debug_toolbar' not in middleware]

# Media files - Keep using Cloudinary as configured in base.py
# Render doesn't provide persistent file storage, so external storage is recommended

# Performance optimizations for production
# Database connection pooling is handled by dj-database-url

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Force HTTPS referrer policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

print(f"🚀 Render settings loaded successfully!")
print(f"📊 Debug mode: {DEBUG}")
print(f"🏠 Allowed hosts: {ALLOWED_HOSTS}")
print(f"🔗 Database: {'PostgreSQL' if DATABASE_URL and 'postgres' in DATABASE_URL else 'SQLite (fallback)'}")
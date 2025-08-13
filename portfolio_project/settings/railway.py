"""
Production settings for Railway deployment.

This file contains settings specific to Railway environment.
Inherits from base.py and overrides/adds Railway-specific configurations.
"""

import dj_database_url
import os

# Set required environment variables before importing base
# This ensures django-environ can read them properly
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-railway-deployment-temp-key-replace-with-secure-key-12345678901234567890'
    print("Warning: Using temporary SECRET_KEY. Set DJANGO_SECRET_KEY or SECRET_KEY environment variable.")

# Ensure environment variables are set before base.py imports
os.environ.setdefault('DJANGO_SECRET_KEY', SECRET_KEY)
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '*')

# Now import base settings
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

# Allowed hosts for Railway
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Add Railway domain if provided
railway_domain = os.environ.get('RAILWAY_STATIC_URL', None)
if railway_domain:
    # Extract domain from Railway static URL
    import urllib.parse
    parsed = urllib.parse.urlparse(railway_domain)
    if parsed.netloc:
        ALLOWED_HOSTS.append(parsed.netloc)

# Ensure Railway and common domains are allowed
if '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '.railway.app', '.up.railway.app'])

# Database configuration for Railway
DATABASE_URL = os.environ.get('DATABASE_URL')

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
else:
    # Fallback to SQLite (not recommended for production)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Override django-environ settings for Railway
# Use os.environ directly since Railway sets environment variables directly
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    # Generate a basic secret key for testing (not secure for production)
    SECRET_KEY = 'django-insecure-railway-deployment-temp-key-replace-with-secure-key-12345678901234567890'
    print("Warning: Using temporary SECRET_KEY. Set DJANGO_SECRET_KEY or SECRET_KEY environment variable.")

# Override the django-environ base setting that prevents ImportError
os.environ.setdefault('DJANGO_SECRET_KEY', SECRET_KEY)

# Email configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@yourportfolio.com')

# Security settings for Railway - be more permissive during initial deployment
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 't')
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 0))  # Start with 0 for initial deployment
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False').lower() in ('true', '1', 't')
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'False').lower() in ('true', '1', 't')

# Cookie security
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() in ('true', '1', 't')
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True').lower() in ('true', '1', 't')
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Additional security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Proxy settings for Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Cache configuration (Redis if available, dummy otherwise)
REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'TIMEOUT': int(os.environ.get('CACHE_TTL', 300)),
            'OPTIONS': {
                'MAX_ENTRIES': int(os.environ.get('CACHE_MAX_ENTRIES', 1000)),
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Static files configuration for Railway
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# WhiteNoise settings for production
WHITENOISE_USE_FINDERS = False
WHITENOISE_AUTOREFRESH = False

# ===== CRITICAL MEDIA FILES CONFIGURATION =====
# Force Cloudinary usage in production - NO FALLBACKS

# Cloudinary is REQUIRED for Railway production
# Check for required Cloudinary environment variables
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')  
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    raise ValueError(
        "Cloudinary credentials are required for Railway deployment. "
        "Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET "
        "in Railway environment variables."
    )

# Configure Cloudinary with secure settings
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,  # Force HTTPS
    )
    
    # Use Cloudinary for all media files
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
    # Cloudinary-specific settings
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
        'SECURE': True,
        'MEDIA_TAG': 'media',
        'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
        'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (),
        'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr', 'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff'],
        'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'manifest'),
        'DEFAULT_FILE_STORAGE': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        'OPTIONS': {
            'resource_type': 'auto',  # Auto-detects images vs raw files
            'type': 'upload', 
            'access_mode': 'public',  # Ensures public access for all files
            'format': 'auto',
            'quality': 'auto:good',
            'fetch_format': 'auto',
        }
    }
    
    # IMPORTANT: NO MEDIA_URL or MEDIA_ROOT for Cloudinary
    # Let Cloudinary handle all URL generation
    # Disable local media completely in production
    print("✅ Cloudinary configured successfully for Railway production")
    
except ImportError as e:
    raise ImportError(
        f"Cloudinary packages are required for Railway deployment: {e}. "
        "Install with: pip install cloudinary django-cloudinary-storage"
    )
except Exception as e:
    raise Exception(f"Failed to configure Cloudinary: {e}")

# Logging configuration for Railway (console only)
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
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'portfolio': {
            'handlers': ['console'],
            'level': os.environ.get('APP_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'cloudinary': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Disable debug toolbar in production
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

# Remove debug middleware
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'debug_toolbar' not in middleware]

# Admin configuration
ADMINS = [
    (os.environ.get('ADMIN_NAME', 'Admin'), os.environ.get('ADMIN_EMAIL', 'admin@example.com')),
]
MANAGERS = ADMINS

# Server email for error notifications
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Data upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('DATA_UPLOAD_MAX_MEMORY_SIZE', 5242880))  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('FILE_UPLOAD_MAX_MEMORY_SIZE', 5242880))  # 5MB

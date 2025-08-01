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


# Override STATICFILES_STORAGE for production to avoid manifest issues
# Use the most basic WhiteNoise storage to avoid any compression conflicts
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

# Disable debug toolbar in production
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')


# Remove debug middleware
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'debug_toolbar' not in middleware]

# Media file serving in production
# Note: Media files are served via WhiteNoise in WSGI for Render compatibility
# For high-traffic production, consider using cloud storage (AWS S3, Cloudinary, etc.)

# File storage configuration
USE_CLOUDINARY = config('USE_CLOUDINARY', default=True, cast=bool)
USE_S3 = config('USE_S3', default=False, cast=bool)

# Check if Cloudinary credentials are available
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default=None)

# Only use Cloudinary if all credentials are provided
if USE_CLOUDINARY and all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    try:
        # Cloudinary configuration (recommended for Render)
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        # Add cloudinary_storage to INSTALLED_APPS if not already there
        if 'cloudinary_storage' not in INSTALLED_APPS:
            INSTALLED_APPS = ['cloudinary_storage'] + INSTALLED_APPS
        if 'cloudinary' not in INSTALLED_APPS:
            INSTALLED_APPS.append('cloudinary')
        
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
            'API_KEY': CLOUDINARY_API_KEY,
            'API_SECRET': CLOUDINARY_API_SECRET,
            'OPTIONS': {
                'secure': True,
                'resource_type': 'auto',
                'folder': 'portfolio',
            }
        }
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )
        
        # Use Cloudinary for media files
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        
        # Cloudinary will handle media URLs directly
        # No need to set MEDIA_URL as Cloudinary provides full URLs
        
        print(f"✓ Cloudinary configured successfully with cloud: {CLOUDINARY_CLOUD_NAME}")
        
    except ImportError:
        print("⚠ Cloudinary not installed, falling back to local media storage")
        USE_CLOUDINARY = False
    except Exception as e:
        print(f"⚠ Cloudinary configuration failed: {e}, falling back to local media storage")
        USE_CLOUDINARY = False
else:
    if USE_CLOUDINARY:
        print("⚠ Cloudinary credentials missing, falling back to local media storage")
    USE_CLOUDINARY = False

# Fallback to local media storage if Cloudinary is not available
if not USE_CLOUDINARY and not USE_S3:
    # Use WhiteNoise to serve media files in production
    # This is not ideal for production but works as a fallback
    print("ℹ Using local media storage with WhiteNoise")
    
    # Ensure media directory exists
    import os
    media_root = BASE_DIR / 'media'
    os.makedirs(media_root, exist_ok=True)
    
    # Use default file storage
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = media_root
    
    # Additional media serving configurations
    # Add media URL patterns for development/fallback serving
    if config('DEBUG', default=False, cast=bool):
        # Only add URL patterns in debug mode
        pass
    else:
        # In production, rely on WhiteNoise configured in wsgi.py
        print(f"Media files will be served from: {MEDIA_ROOT}")
        print(f"Media URL prefix: {MEDIA_URL}")
    
elif USE_S3:
    # AWS S3 or DigitalOcean Spaces configuration
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.StaticS3Boto3Storage'
    
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)  # For DigitalOcean Spaces
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    
    if AWS_S3_CUSTOM_DOMAIN:
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    else:
        STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

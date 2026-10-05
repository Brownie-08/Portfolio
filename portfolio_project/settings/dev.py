"""
Development settings for portfolio_project.

This file contains settings specific to development environment.
Inherits from base.py and overrides/adds development-specific configurations.
"""

from .base import *

# Development settings override base settings
# DEBUG and ALLOWED_HOSTS are already configured in base.py using django-environ
# Additional development-specific overrides can be set here

# Development uses the same SQLite database as PythonAnywhere.
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

# Email backend for development (console output) - already configured in base.py
# EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

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
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
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

# Media files configuration for Cloudinary (development)
# Local development defaults to filesystem media so existing SQLite records
# render from the checked local media directory.
if env.bool('USE_CLOUDINARY_IN_DEV', default=False):
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=env('CLOUDINARY_CLOUD_NAME'),
            api_key=env('CLOUDINARY_API_KEY'),
            api_secret=env('CLOUDINARY_API_SECRET'),
            secure=True  # Force HTTPS
        )
        
        # Use Cloudinary for media files
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        
        # Let Cloudinary handle the MEDIA_URL
        MEDIA_URL = '/media/'  # This will be overridden by Cloudinary
    except (ImportError, AttributeError) as e:
        print(f"Warning: Cloudinary configuration failed: {e}")
        # Fallback to local storage
        import os
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'media'
        os.makedirs(MEDIA_ROOT, exist_ok=True)
else:
    import os
    # Use default Django file storage for media files
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Media files settings
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    # Ensure media directory exists
    os.makedirs(MEDIA_ROOT, exist_ok=True)

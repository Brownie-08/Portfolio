"""
Production settings for Railway deployment.

This file contains streamlined settings for Railway to fix 500 errors.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Import base app configuration
from .base import INSTALLED_APPS, ROOT_URLCONF, WSGI_APPLICATION, AUTH_PASSWORD_VALIDATORS
from .base import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ, DEFAULT_AUTO_FIELD

# Secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-railway-deployment-temp-key-replace-with-secure-key-12345678901234567890'
    print("⚠️  Warning: Using temporary SECRET_KEY. Set DJANGO_SECRET_KEY environment variable in Railway.")

# Debug mode
DEBUG = False

# ✅ Allow Railway domain + wildcard
ALLOWED_HOSTS = ["*", ".railway.app", "localhost", "127.0.0.1"]

# ✅ Database config from Railway
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ✅ Static files (served via WhiteNoise)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <- must be above common middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ Media (resume uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ✅ Confirm Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "portfolio.context_processors.portfolio_context",
            ],
        },
    },
]

# Cloudinary configuration (optional - will fallback to local storage if not available)
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')  
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

# Configure Cloudinary if credentials are available
if all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
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
        
        # Use Cloudinary for default file storage
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        print("✅ Cloudinary configured successfully for Railway production")
        
    except ImportError:
        print("⚠️  Cloudinary packages not installed, using local storage")
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    print("⚠️  Cloudinary credentials not found, using local storage")
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

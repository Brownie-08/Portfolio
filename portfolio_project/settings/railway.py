"""
Production settings for Railway deployment.

This file contains streamlined settings for Railway to fix 500 errors.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core Django Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    # Local apps
    "portfolio",
    "dashboard",
]

# Only add Cloudinary apps if available
try:
    import cloudinary
    import cloudinary_storage
    INSTALLED_APPS.insert(-2, "cloudinary_storage")
    INSTALLED_APPS.insert(-2, "cloudinary")
except ImportError:
    pass

# Django Configuration
ROOT_URLCONF = "portfolio_project.urls"
WSGI_APPLICATION = "portfolio_project.wsgi.application"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-railway-deployment-temp-key-replace-with-secure-key-12345678901234567890'
    print("⚠️  Warning: Using temporary SECRET_KEY. Set DJANGO_SECRET_KEY environment variable in Railway.")

# Debug mode - TEMPORARILY ENABLED FOR DEBUGGING
DEBUG = True

# ✅ Allow Railway domain + wildcard - WILDCARD FOR DEBUGGING
ALLOWED_HOSTS = ['*']

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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

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

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Disable security settings for debugging
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

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
    print("Warning: Using temporary SECRET_KEY. Set DJANGO_SECRET_KEY environment variable in Railway.")

# Debug mode - Use environment variable for production control
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Railway domain configuration for production
RAILWAY_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
    # Also add the full Railway domain format
    if not RAILWAY_DOMAIN.endswith(".railway.app"):
        ALLOWED_HOSTS.append(f"{RAILWAY_DOMAIN}.up.railway.app")
else:
    # Development fallback or when domain not set
    ALLOWED_HOSTS.append("*")

# CSRF trusted origins for Railway
CSRF_TRUSTED_ORIGINS = []
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS = [
        f"https://{RAILWAY_DOMAIN}",
    ]
    # Also add the full Railway domain format for CSRF
    if not RAILWAY_DOMAIN.endswith(".railway.app"):
        CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_DOMAIN}.up.railway.app")
else:
    # Development or fallback - allow common Railway patterns
    CSRF_TRUSTED_ORIGINS = [
        "https://*.up.railway.app",
        "https://*.railway.app",
    ]

# Debug output for Railway configuration
print(f"🚀 Railway Configuration:")
print(f"   DEBUG: {DEBUG}")
print(f"   RAILWAY_DOMAIN: {RAILWAY_DOMAIN or 'Not set'}")
print(f"   ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"   CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")

# ✅ Database config from Railway
# Railway provides DATABASE_URL automatically, fallback to SQLite for local dev
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"📊 DATABASE_URL detected: {'Yes (Postgres)' if DATABASE_URL and 'postgresql' in DATABASE_URL else 'No (using SQLite fallback)'}")

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600,
        ssl_require=False,  # Railway handles SSL automatically
    )
}

# Debug: Print database engine being used
print(f"🔗 Database ENGINE: {DATABASES['default'].get('ENGINE', 'Not configured')}")

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

# Configure media storage strategy
# Use local storage for resumes (to ensure downloadable links work)
# Use Cloudinary for images if available
USE_CLOUDINARY_FOR_IMAGES = all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])

if USE_CLOUDINARY_FOR_IMAGES:
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
        
        print("Cloudinary configured for images, local storage for resumes")
        
    except ImportError:
        print("Cloudinary packages not installed, using local storage for all files")
        USE_CLOUDINARY_FOR_IMAGES = False
else:
    print("Cloudinary credentials not found, using local storage for all files")

# Always use local storage as default to ensure resume downloads work
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Disable security settings for debugging
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

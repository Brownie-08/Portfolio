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

# ✅ Cloudinary Apps - Only add if packages are available and configured
# We'll check credentials later and only configure if both packages and credentials exist
try:
    import cloudinary
    import cloudinary_storage
    # Add cloudinary apps - they'll be configured later when we have credentials
    INSTALLED_APPS.insert(-2, "cloudinary_storage")
    INSTALLED_APPS.insert(-2, "cloudinary")
    print("📦 Cloudinary packages found and added to INSTALLED_APPS")
except ImportError:
    print("ℹ️  Cloudinary packages not installed - using local storage only")

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

# ALLOWED_HOSTS configuration - Railway healthcheck fix
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

# Add Railway domain if present
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)
    # Also add full Railway domain format if needed
    if not railway_domain.endswith(".railway.app"):
        ALLOWED_HOSTS.append(f"{railway_domain}.up.railway.app")

# Allow internal Railway IPs for healthcheck - CRITICAL for Railway
ALLOWED_HOSTS.append(".railway.internal")
ALLOWED_HOSTS.append("*")  # Fallback safety net for Railway healthcheck

# Update RAILWAY_DOMAIN variable to match the environment variable name used above
RAILWAY_DOMAIN = railway_domain

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

# Trust Railway Proxy - CRITICAL for Railway healthcheck
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Debug output for Railway configuration
print(f"🚀 Railway Configuration:")
print(f"   DEBUG: {DEBUG}")
print(f"   RAILWAY_DOMAIN: {RAILWAY_DOMAIN or 'Not set'}")
print(f"   ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"   CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
print(f"   SECURE_PROXY_SSL_HEADER: {SECURE_PROXY_SSL_HEADER}")

# ✅ Database config from Railway
# Railway provides DATABASE_URL automatically for PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and 'postgresql' in DATABASE_URL:
    print(f"📊 DATABASE_URL detected: Yes (PostgreSQL) - {DATABASE_URL[:30]}...")
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,  # Require SSL for PostgreSQL connections
        )
    }
else:
    print(f"📊 DATABASE_URL detected: No (using SQLite fallback for development)")
    print(f"⚠️  PRODUCTION WARNING: PostgreSQL not configured! Add DATABASE_URL to Railway variables.")
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
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

# ✅ Cloudinary Configuration (Robust handling)
# Get Cloudinary credentials from environment
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip()
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '').strip()
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '').strip()
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '').strip()

# Check if we have valid Cloudinary credentials
HAS_CLOUDINARY_CREDENTIALS = bool(
    (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET) or 
    CLOUDINARY_URL
)

# Initialize Cloudinary if we have credentials and packages
USE_CLOUDINARY_FOR_IMAGES = False

if HAS_CLOUDINARY_CREDENTIALS:
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        # Configure Cloudinary
        if CLOUDINARY_URL:
            # Use CLOUDINARY_URL if provided (contains all credentials)
            cloudinary.config(cloudinary_url=CLOUDINARY_URL, secure=True)
        else:
            # Use individual credentials
            cloudinary.config(
                cloud_name=CLOUDINARY_CLOUD_NAME,
                api_key=CLOUDINARY_API_KEY,
                api_secret=CLOUDINARY_API_SECRET,
                secure=True,  # Force HTTPS
            )
        
        USE_CLOUDINARY_FOR_IMAGES = True
        print(f"✅ Cloudinary configured successfully for images (Cloud: {CLOUDINARY_CLOUD_NAME or 'from URL'})")
        print("📁 Local storage will be used for resume downloads")
        
    except ImportError as e:
        print(f"⚠️  Cloudinary packages not available: {e}")
        print("📁 Using local storage for all files")
        USE_CLOUDINARY_FOR_IMAGES = False
        
    except Exception as e:
        print(f"⚠️  Cloudinary configuration failed: {e}")
        print("📁 Falling back to local storage")
        USE_CLOUDINARY_FOR_IMAGES = False
else:
    print("ℹ️  Cloudinary credentials not provided - using local storage for all files")
    print("💡 To enable Cloudinary, set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET")
    print("💡 Or set CLOUDINARY_URL with full connection string")

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

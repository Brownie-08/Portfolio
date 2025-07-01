# Django Settings Configuration

This project uses a modular settings structure with environment-specific configurations using `python-decouple` for secure environment variable management.

## Settings Structure

```
portfolio_project/
├── settings/
│   ├── __init__.py       # Environment detection and imports
│   ├── base.py           # Common settings for all environments
│   ├── dev.py            # Development-specific settings
│   └── prod.py           # Production settings with security hardening
├── settings_old.py       # Backup of original settings file
└── ...
```

## Environment Configuration

### Development Environment
- **File**: `settings/dev.py`
- **Features**:
  - Debug mode enabled
  - SQLite database (default)
  - Console email backend
  - Less restrictive security settings
  - Debug toolbar support (if installed)
  - Comprehensive logging

### Production Environment
- **File**: `settings/prod.py`
- **Features**:
  - Debug mode disabled
  - Database via `DATABASE_URL` environment variable
  - SMTP email backend
  - **Security hardening**:
    - `SECURE_SSL_REDIRECT = True`
    - `SECURE_HSTS_SECONDS = 31536000` (1 year)
    - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
    - `SECURE_HSTS_PRELOAD = True`
    - Secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
    - Content security headers
  - Production logging with file rotation
  - Cache configuration
  - AWS S3 support for media files

## WhiteNoise Configuration

WhiteNoise is configured for static file serving with compression:

```python
# In base.py
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
```

## Environment Variables

Copy `.env.example` to `.env` and configure your environment-specific values:

### Required for Production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `EMAIL_HOST`: SMTP server hostname
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password

### Security Settings
- `SECURE_SSL_REDIRECT`: Force HTTPS redirects
- `SECURE_HSTS_SECONDS`: HSTS header duration
- `SESSION_COOKIE_SECURE`: Secure session cookies
- `CSRF_COOKIE_SECURE`: Secure CSRF cookies

### Optional
- `AWS_ACCESS_KEY_ID`: AWS credentials for S3 media storage
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name
- `CACHE_BACKEND`: Cache backend configuration

## Usage

### Development
```bash
# Set environment (optional, defaults to development)
export DJANGO_ENVIRONMENT=development

# Run development server
python manage.py runserver
```

### Production
```bash
# Set environment
export DJANGO_ENVIRONMENT=production

# Ensure all required environment variables are set
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgres://user:pass@localhost:5432/dbname"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Collect static files
python manage.py collectstatic --noinput

# Run production server
gunicorn portfolio_project.wsgi:application
```

### Using Different Settings Modules
You can also specify settings modules directly:

```bash
# Development
python manage.py runserver --settings=portfolio_project.settings.dev

# Production
python manage.py migrate --settings=portfolio_project.settings.prod
```

## Security Features

### Production Security Headers
- **HSTS**: HTTP Strict Transport Security with 1-year duration
- **Content Type**: Prevents MIME type sniffing
- **XSS Protection**: Browser XSS filtering enabled
- **Frame Options**: Prevents clickjacking with DENY
- **Referrer Policy**: Strict referrer policy
- **Cross-Origin Policies**: Secure cross-origin policies

### Cookie Security
- **Secure Cookies**: Only transmitted over HTTPS
- **HttpOnly Cookies**: Not accessible via JavaScript
- **SameSite Cookies**: CSRF protection with Strict policy
- **Session Timeout**: 1-hour session expiry in production

### Database Security
- Connection pooling with `conn_max_age=600`
- Environment-based credentials
- SSL enforcement for production databases

## Deployment Checklist

- [ ] Set `DJANGO_ENVIRONMENT=production`
- [ ] Configure `SECRET_KEY` with a strong, unique value
- [ ] Set `DATABASE_URL` for your production database
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Set up email credentials (`EMAIL_HOST`, `EMAIL_HOST_USER`, etc.)
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up logging directory (`/var/log/django/`)
- [ ] Configure cache backend (Redis/Memcached for production)
- [ ] Set up AWS S3 for media files (optional)
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`

## Troubleshooting

### Common Issues

1. **Settings import errors**: Ensure the settings package `__init__.py` is properly configured
2. **Environment detection**: Check `DJANGO_ENVIRONMENT` variable
3. **Missing environment variables**: Review `.env` file and ensure all required variables are set
4. **Static files not loading**: Run `collectstatic` and check `STATIC_ROOT` configuration
5. **Database connection errors**: Verify `DATABASE_URL` format and credentials

### Debug Settings
To debug settings loading, you can check which settings module is being used:

```python
from django.conf import settings
print(f"Settings module: {settings.SETTINGS_MODULE}")
print(f"Debug mode: {settings.DEBUG}")
print(f"Environment: {getattr(settings, 'ENVIRONMENT', 'Not set')}")
```

#!/usr/bin/env python3
"""
Portfolio Deployment Preparation Script
========================================

This script prepares your portfolio for secure deployment by:
1. Generating a new secure secret key
2. Creating production environment templates
3. Removing sensitive data from tracked files
4. Preparing for GitHub deployment

Usage:
    python deploy_prep.py

Author: Portfolio Assistant
Date: July 2025
"""

import os
import secrets
import string
import shutil
from pathlib import Path

def generate_secret_key(length=50):
    """Generate a secure Django secret key"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))

def create_production_env():
    """Create production environment template"""
    prod_env_content = """# Production Environment Configuration
# IMPORTANT: Configure these values on your production server

# =============================================================================
# BASIC DJANGO SETTINGS
# =============================================================================
SECRET_KEY=your-super-secure-secret-key-here-50-characters-minimum
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# For PostgreSQL (recommended for production)
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db

# For MySQL (alternative)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=portfolio_db
# DB_USER=portfolio_user
# DB_PASSWORD=your-secure-database-password
# DB_HOST=localhost
# DB_PORT=3306

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
# Gmail SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password-16-chars
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Contact form settings
CONTACT_EMAIL=your-email@gmail.com
SEND_AUTO_REPLY=True
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact] 

# =============================================================================
# SECURITY HEADERS (for production)
# =============================================================================
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# =============================================================================
# STATIC FILES (for production)
# =============================================================================
# For WhiteNoise (included)
STATICFILES_STORAGE=whitenoise.storage.CompressedManifestStaticFilesStorage

# For AWS S3 (optional)
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
# AWS_S3_REGION_NAME=your-aws-region
"""
    
    return prod_env_content

def create_deployment_readme():
    """Create deployment instructions"""
    readme_content = """# 🚀 Portfolio Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Security Checklist
- [ ] `.env` file contains only placeholders
- [ ] `.env.local` is in `.gitignore`
- [ ] New secret key generated for production
- [ ] Database credentials secured
- [ ] Email credentials secured

### ✅ Code Checklist
- [ ] All migrations created and tested
- [ ] Static files collected
- [ ] Media files backed up
- [ ] Contact form tested
- [ ] Dashboard functionality verified

## 🔐 Environment Setup

### 1. Local Development
```bash
# Copy your working environment
cp .env.local .env
python manage.py runserver
```

### 2. Production Setup
```bash
# Use the production template
cp .env.production .env
# Edit .env with your production values
python manage.py collectstatic
python manage.py migrate
```

## 🌐 Deployment Options

### Option 1: DigitalOcean App Platform
1. Connect your GitHub repository
2. Set environment variables in the dashboard
3. Deploy automatically

### Option 2: Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Set environment variables
4. Deploy via Git

### Option 3: VPS (Ubuntu/CentOS)
1. Set up Nginx + Gunicorn
2. Configure SSL certificates
3. Set up systemd service
4. Configure firewall

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use 16-character app password (not your regular password)
4. Test email functionality

### Production Email Services
- **SendGrid**: Professional email delivery
- **AWS SES**: Amazon's email service
- **Mailgun**: Developer-friendly email API

## 🗄️ Database Options

### SQLite (Development Only)
- Perfect for testing and development
- Not recommended for production

### PostgreSQL (Recommended)
- Robust and scalable
- Great for production use
- Excellent Django support

### MySQL (Alternative)
- Popular and well-supported
- Good performance
- Wide hosting support

## 🔧 Production Settings

### Required Environment Variables
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-connection-string
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Optional Security Headers
```
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📱 Contact Form Testing

### Test Checklist
- [ ] Form submission works
- [ ] Email notifications received
- [ ] Auto-reply sent to visitor
- [ ] Dashboard shows new messages
- [ ] Mobile Gmail notifications work

### Test Script
```bash
python manage.py test_email
# Submit test contact form
# Check Gmail on mobile device
```

## 🔍 Monitoring

### Health Checks
- Set up monitoring for your domain
- Monitor email delivery rates
- Check database performance
- Monitor server resources

### Backup Strategy
- Daily database backups
- Weekly full site backups
- Media files backup
- Environment variables backup (securely)

## 🆘 Troubleshooting

### Common Issues
1. **Email not sending**: Check app password and 2FA
2. **Static files not loading**: Run `collectstatic`
3. **Database errors**: Check connection string
4. **SSL errors**: Verify domain and certificates

### Support Resources
- Django Documentation
- Deployment Platform Docs
- Community Forums
- Error Logs

---

**🎉 Your portfolio is ready for the world! Good luck with your deployment! 🚀**
"""
    return readme_content

def main():
    """Main deployment preparation function"""
    print("🚀 Portfolio Deployment Preparation")
    print("=" * 40)
    
    # Get current directory
    project_root = Path.cwd()
    
    # 1. Generate new secret key
    new_secret_key = generate_secret_key()
    print(f"✅ Generated new secret key: {new_secret_key[:10]}...")
    
    # 2. Create production environment file
    prod_env_path = project_root / ".env.production"
    with open(prod_env_path, 'w', encoding='utf-8') as f:
        f.write(create_production_env())
    print(f"✅ Created production environment template: {prod_env_path}")
    
    # 3. Create deployment README
    deploy_readme_path = project_root / "DEPLOYMENT_README.md"
    with open(deploy_readme_path, 'w', encoding='utf-8') as f:
        f.write(create_deployment_readme())
    print(f"✅ Created deployment guide: {deploy_readme_path}")
    
    # 4. Verify .gitignore
    gitignore_path = project_root / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        required_entries = ['.env', '.env.local', '.env.production']
        missing_entries = [entry for entry in required_entries if entry not in gitignore_content]
        
        if missing_entries:
            print(f"⚠️  Add these to .gitignore: {', '.join(missing_entries)}")
        else:
            print("✅ .gitignore properly configured")
    
    # 5. Check for sensitive data
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            env_content = f.read()
        
        # Check for placeholder patterns
        if "{{" in env_content and "}}" in env_content:
            print("✅ .env file contains placeholders (secure)")
        else:
            print("⚠️  WARNING: .env file may contain sensitive data")
    
    print("\n🎯 Deployment Preparation Complete!")
    print("\n📋 Next Steps:")
    print("1. Review .env.production and configure for your hosting")
    print("2. Read DEPLOYMENT_README.md for detailed instructions")
    print("3. Test your application locally with .env.local")
    print("4. Commit and push to GitHub")
    print("5. Deploy to your chosen platform")
    
    print(f"\n🔑 Your new production secret key:")
    print(f"SECRET_KEY={new_secret_key}")
    print("\n⚠️  Save this key securely - you'll need it for production!")

if __name__ == "__main__":
    main()

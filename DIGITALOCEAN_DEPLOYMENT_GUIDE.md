# Django Portfolio Deployment Guide - DigitalOcean

This guide covers deploying your Django portfolio to DigitalOcean using App Platform with MySQL database.

## Prerequisites

- DigitalOcean account
- GitHub repository with your portfolio code
- Domain name (optional but recommended)

## 1. Prepare Your Code for Production

### 1.1 Environment Variables (.env.production)

Create a `.env.production` file (don't commit this):

```bash
# Production Environment Variables
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-app.ondigitalocean.app

# MySQL Database Configuration (DigitalOcean Managed Database)
DB_ENGINE=django.db.backends.mysql
DB_NAME=portfolio_db
DB_USER=doadmin
DB_PASSWORD=your-database-password
DB_HOST=your-database-host.db.ondigitalocean.com
DB_PORT=25060

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Contact form settings
CONTACT_EMAIL=your-email@gmail.com
SEND_AUTO_REPLY=True
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact]

# Security Settings (Production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Optional: DigitalOcean Spaces for file storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-spaces-access-key
AWS_SECRET_ACCESS_KEY=your-spaces-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
AWS_S3_CUSTOM_DOMAIN=your-cdn-domain.com
```

### 1.2 Create Logs Directory

```bash
mkdir logs
echo "# Logs directory for production" > logs/README.md
```

### 1.3 Update Django Settings Module

Update `manage.py` to use production settings by default:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings.production")
```

Or create a `.env` variable:
```bash
DJANGO_SETTINGS_MODULE=portfolio_project.settings.production
```

## 2. DigitalOcean Setup

### 2.1 Create a MySQL Database

1. Log into DigitalOcean Dashboard
2. Go to **Databases** → **Create Database Cluster**
3. Choose:
   - **Database Engine**: MySQL 8
   - **Plan**: Basic ($15/month minimum)
   - **Region**: Choose closest to your users
   - **Database cluster name**: `portfolio-db`

4. After creation, note down:
   - Database name: `defaultdb` (you'll create `portfolio_db`)
   - Username: `doadmin`
   - Password: (provided)
   - Host: `your-cluster-name.db.ondigitalocean.com`
   - Port: `25060`

### 2.2 Set Up Database

Connect to your database and create the portfolio database:

```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portfolio_user'@'%' IDENTIFIED BY 'your-secure-password';
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'%';
FLUSH PRIVILEGES;
```

Or use the default `doadmin` user with `defaultdb` database.

### 2.3 Create App Platform Application

1. Go to **Apps** → **Create App**
2. Choose **GitHub** as source
3. Select your portfolio repository
4. Configure:
   - **Branch**: `feature/complete-portfolio` or `main`
   - **Autodeploy**: Enable for automatic deployments

### 2.4 App Configuration

Create an `app.yaml` file in your repository root:

```yaml
name: django-portfolio
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo-name
    branch: feature/complete-portfolio
    deploy_on_push: true
  run_command: |
    python manage.py collectstatic --noinput
    python manage.py migrate
    gunicorn --worker-tmp-dir /dev/shm portfolio_project.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DJANGO_SETTINGS_MODULE
    value: portfolio_project.settings.production
  - key: SECRET_KEY
    value: your-super-secret-production-key-here
    type: SECRET
  - key: DEBUG
    value: "False"
  - key: ALLOWED_HOSTS
    value: your-domain.com,your-app.ondigitalocean.app
  - key: DB_ENGINE
    value: django.db.backends.mysql
  - key: DB_NAME
    value: portfolio_db
  - key: DB_USER
    value: doadmin
  - key: DB_PASSWORD
    value: your-database-password
    type: SECRET
  - key: DB_HOST
    value: your-database-host.db.ondigitalocean.com
  - key: DB_PORT
    value: "25060"
  - key: EMAIL_BACKEND
    value: django.core.mail.backends.smtp.EmailBackend
  - key: EMAIL_HOST
    value: smtp.gmail.com
  - key: EMAIL_PORT
    value: "587"
  - key: EMAIL_USE_TLS
    value: "True"
  - key: EMAIL_HOST_USER
    value: your-email@gmail.com
  - key: EMAIL_HOST_PASSWORD
    value: your-app-password
    type: SECRET
  - key: DEFAULT_FROM_EMAIL
    value: your-email@gmail.com
  - key: CONTACT_EMAIL
    value: your-email@gmail.com
  http_port: 8080
  routes:
  - path: /
    preserve_path_prefix: false
```

## 3. Domain Setup (Optional)

### 3.1 Add Custom Domain

1. In your App, go to **Settings** → **Domains**
2. Add your domain (e.g., `portfolio.yourdomain.com`)
3. Update DNS records:
   - Create a CNAME record pointing to your app URL
   - Or use A records pointing to DigitalOcean's IP addresses

### 3.2 SSL Certificate

DigitalOcean automatically provides Let's Encrypt SSL certificates for custom domains.

## 4. Deployment Process

### 4.1 Database Migration

After the first deployment, you may need to run migrations manually:

1. In DigitalOcean App Platform, go to **Console**
2. Run:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4.2 Load Initial Data

If you have data from your local SQLite database:

1. Export data from local:
```bash
python manage.py dumpdata --output=initial_data.json --indent=2
```

2. Upload and load in production:
```bash
python manage.py loaddata initial_data.json
```

## 5. File Storage with DigitalOcean Spaces

### 5.1 Create Spaces Bucket

1. Go to **Spaces** → **Create Spaces Bucket**
2. Choose:
   - **Name**: `your-portfolio-media`
   - **Region**: Same as your app
   - **File Listing**: Restricted
   - **CDN**: Enable

### 5.2 Create API Keys

1. Go to **API** → **Spaces Keys**
2. Generate new key pair
3. Note down Access Key and Secret Key

### 5.3 Configure Django for Spaces

Add to your environment variables:

```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your-spaces-access-key
AWS_SECRET_ACCESS_KEY=your-spaces-secret-key
AWS_STORAGE_BUCKET_NAME=your-portfolio-media
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
AWS_S3_CUSTOM_DOMAIN=your-cdn-domain.com  # Optional CDN domain
```

Install additional dependencies:
```bash
pip install boto3 django-storages
```

## 6. Monitoring and Maintenance

### 6.1 Application Metrics

- Monitor app performance in DigitalOcean dashboard
- Set up alerts for downtime or high resource usage

### 6.2 Database Monitoring

- Monitor database performance and storage
- Set up automated backups (DigitalOcean provides daily backups)

### 6.3 Log Monitoring

View application logs in the DigitalOcean App Platform console:
- Runtime logs
- Build logs
- Error logs

## 7. Cost Optimization

### Estimated Monthly Costs:

- **App Platform (Basic)**: $5-12/month
- **Managed MySQL Database**: $15/month (minimum)
- **Spaces (if used)**: $5/month (250GB)
- **CDN**: $1/month (100GB transfer)

**Total**: ~$26-33/month

### Cost Saving Tips:

1. Use the smallest database plan initially
2. Enable CDN only if needed
3. Monitor usage and scale down if possible
4. Use DigitalOcean credits or promotional offers

## 8. Security Checklist

- [ ] Strong SECRET_KEY generated
- [ ] DEBUG=False in production
- [ ] HTTPS enforced
- [ ] Database passwords are secure
- [ ] Email credentials use app passwords
- [ ] Environment variables stored securely
- [ ] Regular security updates
- [ ] Monitor for suspicious activity

## 9. Troubleshooting

### Common Issues:

1. **Database Connection Errors**
   - Check database credentials
   - Verify database is in same region
   - Check firewall settings

2. **Static Files Not Loading**
   - Run `collectstatic` command
   - Check STATIC_URL and STATIC_ROOT settings
   - Verify Spaces configuration if using

3. **Email Not Working**
   - Check Gmail app password
   - Verify SMTP settings
   - Check firewall/port restrictions

4. **Domain Issues**
   - Verify DNS records
   - Check SSL certificate status
   - Allow time for DNS propagation

## 10. Maintenance Commands

### Useful Django management commands for production:

```bash
# Check system
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Clear cache (if using Redis)
python manage.py clear_cache

# Check database
python manage.py dbshell
```

This guide should help you successfully deploy your Django portfolio to DigitalOcean App Platform. Remember to test thoroughly before pointing your domain to production!

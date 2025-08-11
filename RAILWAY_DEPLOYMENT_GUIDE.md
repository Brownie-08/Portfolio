# 🚂 Railway Deployment Guide for Django Portfolio

## 🎯 **Quick Deployment Steps**

### **Step 1: Prepare Your Project**
✅ **Already Done!** Your project is now Railway-ready with:
- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `nixpacks.toml` - Build configuration
- `.env.railway` - Environment variables template
- Production settings configured for MySQL

### **Step 2: Push to GitHub**
```bash
# Make sure all changes are committed
git add .
git commit -m "🚂 Add Railway deployment configuration"
git push origin main
```

### **Step 3: Set Up Railway Project**

#### **A. Create Railway Account & Project**
1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your portfolio repository
5. Railway will automatically detect it's a Django project

#### **B. Add MySQL Database**
1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"MySQL"**
3. Railway will create a MySQL instance and provide connection details
4. Copy the **DATABASE_URL** from the MySQL service

#### **C. Configure Environment Variables**
In your Railway project, go to **Variables** tab and add these:

```env
SECRET_KEY=your-secure-django-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio_project.settings.railway
ALLOWED_HOSTS=*

# 🖼️ CLOUDINARY CONFIGURATION (CRITICAL FOR IMAGE UPLOADS)
# BOTH variables required - this fixes admin dashboard image uploads
USE_CLOUDINARY=True
USE_LOCAL_STORAGE=False
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=your-email@yahoo.com
CONTACT_EMAIL=your-email@yahoo.com
SEND_AUTO_REPLY=True
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact] 

# Security Settings
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Important:** 
- The `DATABASE_URL` will be automatically set by Railway's MySQL plugin
- Replace placeholder values with your actual credentials:
  - Get Cloudinary credentials from your [Cloudinary Dashboard](https://cloudinary.com/console)
  - Use a secure Django secret key (generate one at [djecrety.ir](https://djecrety.ir/))
  - Use your actual email credentials for SMTP configuration

### **Step 4: Deploy**
1. Railway will automatically deploy when you push to GitHub
2. First deployment includes:
   - Installing Python dependencies
   - Running database migrations
   - Collecting static files
   - Starting gunicorn server

### **Step 5: Create Superuser**
After successful deployment:
1. Go to your Railway project dashboard
2. Click on your web service
3. Go to **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"** and then **"Terminal"**
6. Run: `python manage.py createsuperuser`

---

## 🔍 **Testing Your Deployment**

### **✅ Checklist**
Visit your Railway URL (found in project dashboard) and verify:

- [ ] **Homepage loads** - Hero section, projects, testimonials
- [ ] **About page** - Biography, skills, education, certifications
- [ ] **Projects page** - Portfolio showcase
- [ ] **Blog page** - Posts and navigation
- [ ] **Contact form** - Form submission and email notifications
- [ ] **Dashboard** - Admin interface at `/dashboard/`
- [ ] **Static files** - CSS, JS, images load correctly
- [ ] **Media files** - Uploaded images display properly

### **📧 Email Testing**
1. Submit a test contact form
2. Check your Gmail for notification
3. Verify auto-reply was sent
4. Check dashboard for new message

### **🖼️ Image Upload Testing (CRITICAL)**
**This deployment fixes the broken image upload issue!**

1. **Login to Admin Dashboard**: `/dashboard/login/`
2. **Upload Test Image**: 
   - Go to Projects → Add New Project
   - Upload a project image
   - Save the project
3. **Verify Cloudinary Storage**:
   - Image URL should contain `res.cloudinary.com`
   - Image displays correctly immediately
   - Image persists after Railway redeployment
4. **Test Persistence**:
   - Wait for automatic redeployment or trigger one
   - Verify uploaded images still display (they will!)

**Before this fix**: Images disappeared after redeployment  
**After this fix**: Images stored on Cloudinary and persist forever ✅

---

## 🌐 **Custom Domain Setup (Optional)**

### **Connect Your Domain**
1. In Railway project, go to **"Settings"** → **"Domains"**
2. Click **"+ Custom Domain"**
3. Enter your domain (e.g., `portfolio.yourdomain.com`)
4. Add the provided CNAME record to your DNS settings
5. Railway will automatically provision SSL certificate

### **Update Environment Variables**
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,portfolio.yourdomain.com
SECURE_SSL_REDIRECT=True
```

---

## 🛠️ **Railway-Specific Features**

### **Automatic Deployments**
- Every push to `main` branch triggers automatic deployment
- Zero-downtime deployments
- Automatic rollback on failure

### **Built-in Monitoring**
- Real-time logs and metrics
- Resource usage monitoring
- Uptime monitoring

### **Scaling**
- Automatic scaling based on traffic
- Resource optimization
- Global CDN for static files

---

## 🔧 **Environment Variables Reference**

### **Required Variables**
```env
SECRET_KEY                    # Django secret key
DEBUG                        # False for production
DJANGO_SETTINGS_MODULE       # portfolio_project.settings.production
DATABASE_URL                 # Auto-generated by MySQL plugin
EMAIL_HOST_USER              # Your Gmail address
EMAIL_HOST_PASSWORD          # Gmail app password
```

### **Optional Variables**
```env
ALLOWED_HOSTS               # Comma-separated domains
SECURE_SSL_REDIRECT         # True for HTTPS redirect
CONTACT_EMAIL              # Where contact forms are sent
SEND_AUTO_REPLY            # Enable auto-reply emails
USE_S3                     # False to use WhiteNoise
REDIS_URL                  # For caching (optional)
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Database Connection Error**
- Verify MySQL plugin is running
- Check DATABASE_URL is set correctly
- Ensure migrations ran successfully

#### **2. Static Files Not Loading**
- Check `collectstatic` ran during deployment
- Verify WhiteNoise is in MIDDLEWARE
- Check STATIC_ROOT setting

#### **3. Email Not Sending**
- Verify Gmail app password is correct
- Check EMAIL_HOST_PASSWORD environment variable
- Ensure 2FA is enabled on Gmail account

#### **4. 500 Internal Server Error**
- Check deployment logs for errors
- Verify all environment variables are set
- Check Django settings configuration

### **Debugging Commands**
Access Railway terminal and run:
```bash
# Check Django configuration
python manage.py check

# Test database connection
python manage.py dbshell

# Check migrations
python manage.py showmigrations

# Test email configuration
python manage.py test_email

# Collect static files manually
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

---

## 📊 **Performance Optimization**

### **Railway Best Practices**
- Use WhiteNoise for static files (already configured)
- Enable gzip compression (Railway does this automatically)
- Optimize database queries
- Use select_related() and prefetch_related()
- Enable browser caching

### **Monitoring**
- Monitor response times in Railway dashboard
- Check resource usage and scale if needed
- Set up uptime monitoring
- Review error logs regularly

---

## 🎉 **Success!**

Your Django portfolio is now live on Railway with:
- ✅ **MySQL Database** - Fully managed and backed up
- ✅ **Automatic HTTPS** - SSL certificate included
- ✅ **Professional Email** - Gmail integration working
- ✅ **Auto Deployments** - Push to deploy
- ✅ **Production Ready** - Optimized and secure

**🌐 Your portfolio is now accessible to the world!**

**📧 Email notifications will be sent to your Gmail whenever someone contacts you.**

**🔗 Share your Railway URL with potential clients and employers!**

---

## 📞 **Support**

### **Railway Documentation**
- [Railway Docs](https://docs.railway.app/)
- [Django on Railway](https://docs.railway.app/guides/django)
- [MySQL Plugin](https://docs.railway.app/plugins/mysql)

### **Project Documentation**
- `README.md` - Project overview
- `DEPLOYMENT_README.md` - General deployment guide
- `PROJECT_COMPLETION_SUMMARY.md` - Feature overview

**🚂 Happy deploying with Railway! 🎉**

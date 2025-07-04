# 🌐 Render.com Environment Variables Configuration

## 📋 **Required Environment Variables for Render**

Set these **exactly** in your Render.com service settings:

### **🔑 Core Django Settings**
```
SECRET_KEY=$jEz6MT0T%Vx$DAu#uXLY#*08s^NnF$=+m^q4O&%fAZ@Na0OXc
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio_project.settings.production
PYTHON_VERSION=3.11.4
```

### **🌐 Host Configuration**
```
ALLOWED_HOSTS=*
```

### **📧 Email Configuration (Gmail)**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=udohpeterbrown@gmail.com
EMAIL_HOST_PASSWORD=YOUR_NEW_16_CHAR_APP_PASSWORD
DEFAULT_FROM_EMAIL=udohpeterbrown@gmail.com
CONTACT_EMAIL=udohpeterbrown@gmail.com
SEND_AUTO_REPLY=True
ADMIN_EMAIL_SUBJECT_PREFIX=[Portfolio Contact] 
```

### **🔒 Security Settings (Render Optimized)**
```
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🗄️ **Database Options**

### **Option 1: PostgreSQL (Recommended)**
Render provides free PostgreSQL:
- Create PostgreSQL database in Render
- Use the generated `DATABASE_URL` automatically

### **Option 2: SQLite (Fallback)**
For testing only - not recommended for production:
```
DATABASE_URL=sqlite:///db.sqlite3
```

---

## ⚠️ **IMPORTANT NOTES**

### **📧 Email Password**
- Replace `YOUR_NEW_16_CHAR_APP_PASSWORD` with your **NEW** Gmail app password
- Use the 16-character password, not your regular Gmail password

### **🌐 Domain Configuration**
- `ALLOWED_HOSTS=*` allows Render to route traffic properly
- Render automatically provides your app domain (yourapp.onrender.com)

### **🔒 Security**
- Render provides automatic HTTPS, so SSL redirect is enabled
- All security headers are enabled for production

---

## 🎯 **How to Set Variables in Render**

### **During Service Creation:**
1. Go to [Render.com](https://render.com) and sign up/login
2. Connect your GitHub account
3. Click **"New"** → **"Web Service"**
4. Select your portfolio repository
5. Fill in the build/start commands (see below)
6. Add environment variables in the **"Environment"** section

### **Build & Start Commands:**
```bash
# Build Command:
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command:
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$PORT
```

### **After Service Creation:**
1. Go to your service dashboard
2. Click **"Environment"** tab
3. Add each variable with **"Add Environment Variable"**
4. Service will auto-redeploy when you save

---

## ✅ **Verification Checklist**

Before deploying:
- [ ] All 15+ environment variables are set
- [ ] SECRET_KEY uses the production key
- [ ] DEBUG=False
- [ ] EMAIL_HOST_PASSWORD uses your NEW app password
- [ ] Build and start commands are correct
- [ ] Database option selected (PostgreSQL recommended)

---

## 🚀 **Ready for Render Deployment**

Once all variables are configured, Render will:
1. Build your application (2-3 minutes)
2. Run migrations and collect static files
3. Start your Django application
4. Provide HTTPS URL automatically
5. Monitor health and restart if needed

Your portfolio will be live at: `https://yourapp.onrender.com`

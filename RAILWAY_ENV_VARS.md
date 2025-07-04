# 🚂 Railway Environment Variables Configuration

## 📋 **Required Environment Variables for Railway**

Copy and paste these **exactly** into your Railway project Variables tab:

### **🔑 Core Django Settings**
```
SECRET_KEY=$jEz6MT0T%Vx$DAu#uXLY#*08s^NnF$=+m^q4O&%fAZ@Na0OXc
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio_project.settings.production
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

### **🔒 Security Settings (Railway Optimized)**
```
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### **📊 Logging & Performance**
```
DJANGO_LOG_LEVEL=INFO
```

---

## ⚠️ **IMPORTANT NOTES**

### **🗄️ Database Configuration**
- **DATABASE_URL** is automatically set by Railway's MySQL plugin
- **DO NOT** manually add DATABASE_URL - Railway handles this

### **📧 Email Password**
- Replace `YOUR_NEW_16_CHAR_APP_PASSWORD` with your **NEW** Gmail app password
- Use the 16-character password, not your regular Gmail password

### **🌐 Domains**
- `ALLOWED_HOSTS=*` allows Railway to route traffic properly
- Railway handles SSL termination, so secure cookies are disabled

---

## 🎯 **How to Set Variables in Railway**

1. **Go to your Railway project dashboard**
2. **Click on your web service**
3. **Go to "Variables" tab**
4. **Add each variable one by one:**
   - Variable Name: `SECRET_KEY`
   - Variable Value: `$jEz6MT0T%Vx$DAu#uXLY#*08s^NnF$=+m^q4O&%fAZ@Na0OXc`
   - Click "Add"
5. **Repeat for all variables above**

---

## ✅ **Verification Checklist**

After setting all variables:
- [ ] SECRET_KEY is set with the production key
- [ ] DEBUG=False
- [ ] EMAIL_HOST_PASSWORD uses your NEW app password
- [ ] DJANGO_SETTINGS_MODULE points to production settings
- [ ] All 13 variables are configured

---

## 🚀 **Ready for Deployment**

Once all variables are set, Railway will automatically redeploy your application with the new configuration.

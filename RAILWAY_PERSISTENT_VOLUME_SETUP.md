# 🚂 Railway Persistent Volume Setup Guide

## 📌 **Goal: Resume Upload & Auto-Delete System**

✅ Admin can upload/update resume from dashboard  
✅ Files stored in Railway persistent volume  
✅ Public can view/download latest file  
✅ Old resumes auto-deleted when new ones uploaded  
✅ **NO 401 errors or Cloudinary issues!**

---

## **1️⃣ Railway Persistent Volume Setup**

### **Step 1: Enable Persistent Storage**

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Navigate to your project
   - Select your service

2. **Enable Volume**
   - Go to **Settings** → **Volumes**
   - Click **"+ New Volume"**
   - Set **Mount Path**: `/app/media`
   - Set **Size**: `1GB` (more than enough for resume files)
   - Click **Create Volume**

3. **Redeploy**
   - Railway will automatically redeploy with the new volume
   - Wait for deployment to complete

---

## **2️⃣ Verify Settings (Already Configured)**

Your settings are already configured in `settings/railway.py`:

```python
# Railway Persistent Volume Detection
if os.path.exists('/app/media'):
    MEDIA_ROOT = '/app/media'  # Railway persistent volume
    print("Using Railway persistent volume for media files")
else:
    MEDIA_ROOT = BASE_DIR / 'media'  # Local development
    print("Using local media directory")

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

---

## **3️⃣ How It Works**

### **Auto-Delete Logic (Already Implemented)**

When you upload a new resume through the Django admin:

```python
def save(self, *args, **kwargs):
    # Auto-delete old resume when uploading new one
    if self.pk:  # Existing record
        try:
            old_instance = PersonalInfo.objects.get(pk=self.pk)
            if old_instance.resume and self.resume and old_instance.resume.name != self.resume.name:
                # Delete old file from Railway persistent volume
                if os.path.isfile(old_instance.resume.path):
                    os.remove(old_instance.resume.path)
        except Exception as e:
            logger.warning(f"Could not delete old resume: {e}")
    
    super().save(*args, **kwargs)
```

### **Resume Serving (Already Implemented)**

Public access via:
- Direct URL: `https://your-site.com/media/files/resume.pdf`
- Fallback view: `https://your-site.com/resume-download/`

---

## **4️⃣ Usage Workflow**

### **For Admin (You):**

1. **Upload Resume**
   - Go to Django Admin: `https://your-site.com/admin/`
   - Navigate to **Portfolio → Personal Infos**
   - Click on your personal info entry
   - Upload new resume file in the **Resume** field
   - Click **Save**

2. **Auto-Magic Happens**
   - ✅ Old resume file automatically deleted
   - ✅ New resume file saved to Railway persistent volume
   - ✅ Public links immediately work
   - ✅ No deployment needed!

### **For Public (Visitors):**

1. **Download Resume**
   - Click "Download CV" button on your site
   - File downloads directly from Railway persistent volume
   - No 401 errors, no authentication required
   - Always gets the latest uploaded resume

---

## **5️⃣ Benefits of This Approach**

✅ **No 401 Access Issues** - Files served directly by Django  
✅ **No Cloudinary Needed** - Self-contained solution  
✅ **Auto-Cleanup** - Old files deleted automatically  
✅ **One-Click Updates** - Upload new resume instantly  
✅ **Persistent Storage** - Files survive deployments  
✅ **Cost Effective** - 1GB Railway volume is very cheap  
✅ **Fast Delivery** - Files served from Railway's CDN  

---

## **6️⃣ File Locations**

### **Development:**
- Files stored in: `C:\Users\User\My Porfolio\media\files\`

### **Production (Railway):**
- Files stored in: `/app/media/files/`
- Mounted from Railway persistent volume
- Survives all deployments and restarts

---

## **7️⃣ Troubleshooting**

### **If Resume Download Still Shows 401:**

1. **Check Volume Mount**
   ```bash
   # SSH into Railway container (if available)
   ls -la /app/media/
   ```

2. **Check File Permissions**
   ```bash
   # In Railway console
   python manage.py test_resume_download
   ```

3. **Re-upload Resume**
   - Delete current resume from Django admin
   - Upload a new one
   - This triggers the auto-delete logic

### **Common Issues:**

- **Volume Not Mounted**: Railway volume not properly configured
- **File Not Found**: Resume not uploaded through Django admin
- **Permission Issues**: Railway container permissions

---

## **8️⃣ Testing Your Setup**

### **After Railway Deploys:**

1. **Upload a test resume** via Django admin
2. **Visit your site** and click "Download CV"
3. **File should download immediately** without any 401 errors
4. **Upload another resume** - old one should be auto-deleted

### **Expected File Structure:**
```
/app/media/
├── files/
│   └── your-resume.pdf
├── images/
│   ├── profile/
│   ├── projects/
│   └── testimonials/
```

---

## **9️⃣ Success Criteria**

✅ Resume uploads work in Django admin  
✅ Public can download resume without authentication  
✅ Old resume files are automatically deleted  
✅ No 401 or 403 errors  
✅ Files persist through deployments  
✅ Fast download speeds  

**Your Railway persistent volume setup is now complete! 🎉**

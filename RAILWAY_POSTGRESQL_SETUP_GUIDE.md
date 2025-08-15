# 🐘 Railway PostgreSQL Setup Guide - Fix Database Issues

This guide will help you switch from SQLite to PostgreSQL on Railway to fix your admin login and data persistence issues.

## 🚨 **Why You Need This**

Your current issue: Django is falling back to SQLite because DATABASE_URL isn't properly configured.

**Symptoms:**
- Admin users disappear after deployment
- Data doesn't persist between deploys  
- Logs show: `📊 DATABASE_URL detected: No (using SQLite fallback)`
- Your PostgreSQL data isn't visible in production

## 🔧 **Step-by-Step Fix**

### Step 1: Add PostgreSQL Plugin to Railway

1. **Go to your Railway project dashboard**
2. **Click "Add Service" or the `+` button**
3. **Select "Database" → "Add PostgreSQL"**
4. **Wait for PostgreSQL to deploy** (takes ~30 seconds)

### Step 2: Get Your DATABASE_URL

1. **Click on your PostgreSQL service** in Railway dashboard
2. **Go to "Variables" tab**
3. **Copy the `DATABASE_URL`** - it looks like:
   ```
   postgresql://postgres:password@server:5432/railway
   ```

### Step 3: Add DATABASE_URL to Your Django App

1. **Go to your Django service** (not the PostgreSQL service)
2. **Click "Variables" tab**
3. **Add new variable:**
   - **Name:** `DATABASE_URL`
   - **Value:** `[paste the PostgreSQL URL you copied]`

### Step 4: Add Required Environment Variables

Add these variables to your Django service:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@server:5432/railway

# Superuser credentials
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@domain.com
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!

# Security (optional but recommended)
DJANGO_SECRET_KEY=your-super-long-secret-key-here-50-plus-characters
```

### Step 5: Deploy and Verify

1. **Your app will automatically redeploy**
2. **Check deployment logs** - you should see:
   ```
   📊 DATABASE_URL detected: Yes (PostgreSQL) - postgresql://...
   🔗 Database ENGINE: django.db.backends.postgresql
   ✅ Superuser 'admin' created/updated with fresh credentials!
   ```

## 🎯 **Verification Checklist**

### ✅ Check Deployment Logs
Look for these success messages:
- `📊 DATABASE_URL detected: Yes (PostgreSQL)`
- `Migrations completed`
- `✅ Superuser 'admin' created/updated`

### ✅ Test Admin Login
1. Go to: `https://your-app.up.railway.app/admin/`
2. Login with your Railway environment variables
3. Verify you have admin access

### ✅ Data Persistence Test
1. Add some data through admin
2. Trigger a redeploy
3. Check if data persists after deployment

## 🔍 **Troubleshooting**

### Problem: Still seeing SQLite in logs?

**Solution:** Double-check your DATABASE_URL variable:
- Is it set in the **Django service** (not PostgreSQL service)?
- Does it start with `postgresql://`?
- Are there any typos?

### Problem: Connection errors?

**Solution:** Check PostgreSQL service status:
- Is the PostgreSQL service running?
- Try regenerating the DATABASE_URL from Railway

### Problem: Superuser not created?

**Solution:** Check environment variables:
- Are `DJANGO_SUPERUSER_*` variables set in Django service?
- Check deployment logs for error messages

### Problem: Data from old app not showing?

**Solution:** Your old SQLite data won't transfer automatically:
- Option 1: Export data from local SQLite, import to PostgreSQL
- Option 2: Recreate data through Django admin
- Option 3: Use Django fixtures (`loaddata` command)

## 🚀 **Expected Results After Setup**

### ✅ **Database Connection**
```
📊 DATABASE_URL detected: Yes (PostgreSQL) - postgresql://...
🔗 Database ENGINE: django.db.backends.postgresql
```

### ✅ **Superuser Creation**
```
✅ Superuser 'admin' updated with fresh credentials!
📧 Email: your-email@domain.com
🎯 Password updated from Railway environment variables
```

### ✅ **Persistent Data**
- Admin users persist between deployments
- All data stored in PostgreSQL remains available
- No more data loss on redeploys

## 🔒 **Security Best Practices**

1. **Use strong passwords** for `DJANGO_SUPERUSER_PASSWORD`
2. **Set a unique SECRET_KEY** (50+ characters)
3. **Use a real email** for `DJANGO_SUPERUSER_EMAIL`
4. **Never commit credentials** to your code repository

## 📋 **Quick Copy-Paste Environment Variables**

```bash
# Required for PostgreSQL connection
DATABASE_URL=postgresql://[your-db-url-from-railway]

# Required for auto-superuser creation  
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!

# Recommended
DJANGO_SECRET_KEY=your-very-long-secret-key-minimum-50-characters-random-string-here
DEBUG=False
```

## 🎉 **Success!**

Once completed, your Django app will:
- ✅ Use persistent PostgreSQL database
- ✅ Auto-create/update superuser on every deploy
- ✅ Maintain data between deployments
- ✅ Allow reliable admin access at `/admin/`

Your admin login issues should be completely resolved! 🚀

---

## 🆘 **Still Having Issues?**

If you're still seeing problems:

1. **Check Railway service logs** for specific error messages
2. **Verify all environment variables** are set correctly
3. **Ensure PostgreSQL service is running** in Railway dashboard
4. **Try redeploying** after setting all variables

The most common issue is forgetting to add the DATABASE_URL to the **Django service** instead of the PostgreSQL service.

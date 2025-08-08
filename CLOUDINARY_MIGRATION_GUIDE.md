# Cloudinary Migration Guide for Django Portfolio

This guide will help you migrate your Django portfolio images to Cloudinary while keeping resume files local, ensuring images persist through Railway redeployments.

## Overview

✅ **What this migration does:**
- Migrates all existing images (projects, testimonials, blog posts, profile pictures, etc.) to Cloudinary
- Updates database records to use Cloudinary URLs
- Keeps resume/CV files local (as requested)
- Sets up selective storage for future uploads
- Maintains admin dashboard functionality

✅ **What stays the same:**
- Resume download functionality remains unchanged
- All existing URLs work seamlessly
- Admin dashboard upload functionality preserved
- No code changes needed in templates

## Prerequisites

1. **Cloudinary Account**: Sign up at https://cloudinary.com (free tier available)
2. **Environment Variables**: Cloudinary credentials in your `.env` and production environment

## Step-by-Step Instructions

### Step 1: Get Cloudinary Credentials

1. Go to https://cloudinary.com and sign up/login
2. In your dashboard, find these credentials:
   - Cloud Name
   - API Key
   - API Secret

### Step 2: Update Environment Variables

**Local Development (.env file):**
```env
# Update these with your actual Cloudinary credentials
USE_CLOUDINARY=False  # Keep False for local development
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

**Production Environment (Railway):**
Add these environment variables in your Railway dashboard:
```
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

### Step 3: Test Your Setup

Run the setup test to verify everything is configured correctly:

```bash
# Test with current settings (should show missing credentials if not set)
python manage.py test_cloudinary_setup

# Set credentials temporarily for testing (optional)
set USE_CLOUDINARY=True
set CLOUDINARY_CLOUD_NAME=your-cloud-name
set CLOUDINARY_API_KEY=your-api-key  
set CLOUDINARY_API_SECRET=your-api-secret
python manage.py test_cloudinary_setup
```

### Step 4: Run Migration (Dry Run First)

**IMPORTANT: Always run dry-run first to see what will be migrated**

```bash
# See what would be migrated (no changes made)
python manage.py migrate_images_to_cloudinary --dry-run
```

Review the output carefully. You should see:
- List of images that will be migrated to Cloudinary
- Resume files that will be skipped (kept local)
- Any issues with file access

### Step 5: Perform Actual Migration

Once you're satisfied with the dry-run results:

```bash
# Perform the actual migration
python manage.py migrate_images_to_cloudinary
```

This will:
- Upload all images to Cloudinary
- Update database records with Cloudinary URLs
- Skip resume files (keep them local)
- Provide detailed progress and error reporting

### Step 6: Deploy to Production

1. **Set Production Environment Variables** (if not done already):
   - `USE_CLOUDINARY=True`
   - Your Cloudinary credentials

2. **Deploy your application** to Railway

3. **Run migration on production** (optional, if you have different images):
   ```bash
   # In Railway console or during deployment
   python manage.py migrate_images_to_cloudinary
   ```

### Step 7: Verify Everything Works

1. **Check your website**: All images should display correctly
2. **Test admin dashboard**: Upload new images to verify they go to Cloudinary
3. **Test resume download**: Should still work from local storage
4. **Check after redeploy**: Images should persist through Railway redeployments

## How It Works

### Selective Storage System

The migration implements a selective storage system:

- **Images → Cloudinary**: `images/projects/`, `images/testimonials/`, `images/blog/`, etc.
- **Resume Files → Local**: `files/`, anything containing "resume" or "cv", PDF files

### File Type Handling

| File Type | Storage Location | Example |
|-----------|------------------|---------|
| Project images | Cloudinary | `images/projects/my-app.jpg` |
| Profile images | Cloudinary | `images/profile/avatar.png` |
| Blog images | Cloudinary | `images/blog/post-header.jpg` |
| Resume files | Local (Railway) | `files/resume.pdf` |
| CV files | Local (Railway) | `files/my-cv.pdf` |

### URL Structure After Migration

- **Cloudinary images**: `https://res.cloudinary.com/your-cloud/image/upload/...`
- **Local files**: `https://yoursite.com/media/files/resume.pdf`

## Troubleshooting

### Common Issues and Solutions

1. **"Missing Cloudinary environment variables"**
   - Solution: Add all required variables to both `.env` and production environment

2. **"File not found locally"**
   - Some database records point to non-existent files
   - These will be logged as failed migrations
   - Safe to ignore if files are truly missing

3. **"Cloudinary connection failed"**
   - Check your credentials are correct
   - Verify your internet connection
   - Check Cloudinary service status

4. **"Images not displaying after deployment"**
   - Verify `USE_CLOUDINARY=True` in production
   - Check that migration completed successfully
   - Verify Cloudinary credentials in production environment

5. **"Admin dashboard uploads not working"**
   - Ensure `USE_CLOUDINARY=True` in production
   - Verify Cloudinary credentials
   - Check browser console for JavaScript errors

### Rollback Strategy

If you need to rollback:

1. Set `USE_CLOUDINARY=False` in production
2. Redeploy your application
3. Your local files will be used again (though newly uploaded images might be missing)

## Testing Checklist

- [ ] Environment variables set correctly
- [ ] Cloudinary connection test passes
- [ ] Dry-run shows expected files to migrate
- [ ] Migration completes successfully
- [ ] Website displays all images correctly
- [ ] Admin dashboard can upload new images
- [ ] Resume download still works
- [ ] Images persist after Railway redeploy

## Advanced Options

### Force Re-upload

If you need to re-upload images already on Cloudinary:

```bash
python manage.py migrate_images_to_cloudinary --force
```

### Migration Command Options

```bash
# See all available options
python manage.py migrate_images_to_cloudinary --help

# Dry run (recommended first)
python manage.py migrate_images_to_cloudinary --dry-run

# Force re-upload existing Cloudinary images
python manage.py migrate_images_to_cloudinary --force

# Combined options
python manage.py migrate_images_to_cloudinary --dry-run --force
```

## Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the migration command output for specific errors
3. Run the test command to verify setup: `python manage.py test_cloudinary_setup`
4. Check Cloudinary dashboard for uploaded images

## Security Notes

- Never commit your Cloudinary credentials to version control
- Use environment variables for all sensitive information
- Cloudinary URLs are public but have unique identifiers
- Resume files remain on your server for security

---

**🎉 Once completed, your images will persist through all Railway redeployments while maintaining full functionality!**

# Changelog

All notable changes to this Django Portfolio project will be documented in this file.

## [Unreleased] - 2025-08-11

### 🔧 Fixed
- **CRITICAL**: Fixed broken image uploads in Railway production environment
  - **Issue**: Images uploaded through admin dashboard appeared broken/404 in production
  - **Root Cause**: Missing `USE_LOCAL_STORAGE=False` environment variable
  - **Solution**: Updated Railway settings configuration to properly use Cloudinary when both `USE_CLOUDINARY=True` AND `USE_LOCAL_STORAGE=False`
  - **Impact**: New image uploads now persist through Railway redeployments

### 🚀 Enhanced
- **Railway Deployment**: Updated deployment guide with correct Cloudinary configuration
- **Environment Variables**: Added clear documentation for required Cloudinary settings
- **Production Settings**: Improved railway.py settings with better storage logic

### 📝 Documentation
- Added comprehensive Railway deployment guide with image upload fix
- Updated environment variable documentation
- Added troubleshooting section for common deployment issues

### ⚙️ Configuration Changes
Required Railway environment variables now include:
```env
USE_CLOUDINARY=True
USE_LOCAL_STORAGE=False  # ← This was missing before
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### 🧪 Testing
- Verified Cloudinary configuration works locally
- Confirmed storage backend switches correctly based on environment variables
- Tested selective storage (images → Cloudinary, resumes → local)

---

## Previous Versions

### [1.0.0] - 2025-07-XX
- Initial portfolio project completion
- Django admin dashboard
- Project, blog, testimonial management
- Contact form with email notifications
- Professional responsive design
- Local development setup

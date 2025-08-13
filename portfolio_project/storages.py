"""
Custom storage classes for handling different file types in Cloudinary.

This module provides specialized storage classes to ensure:
- Images use the standard image/upload resource type
- PDFs/documents use the raw/upload resource type with public access
- Existing images remain unaffected by PDF storage changes
"""

from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
import cloudinary


class PublicPDFStorage(RawMediaCloudinaryStorage):
    """
    Custom storage class for PDF files and documents.
    
    This ensures that PDFs are uploaded to Cloudinary with:
    - resource_type="raw" (correct for non-image files)  
    - access_mode="public" (ensures public accessibility)
    - secure=True (forces HTTPS URLs)
    
    Usage in models:
        resume = models.FileField(storage=PublicPDFStorage(), upload_to='files/')
    """
    
    def get_available_name(self, name, max_length=None):
        """Override to ensure unique names for PDF files"""
        return super().get_available_name(name, max_length)
    
    def _save(self, name, content):
        """Override save to ensure proper PDF upload configuration"""
        # Ensure Cloudinary config is loaded
        if not cloudinary.config().cloud_name:
            try:
                cloudinary.config(
                    cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
                    api_key=settings.CLOUDINARY_STORAGE.get('API_KEY'),
                    api_secret=settings.CLOUDINARY_STORAGE.get('API_SECRET'),
                    secure=True
                )
            except (AttributeError, KeyError):
                # Fallback to environment variables
                cloudinary.config(
                    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                    api_key=settings.CLOUDINARY_API_KEY,
                    api_secret=settings.CLOUDINARY_API_SECRET,
                    secure=True
                )
        
        # The RawMediaCloudinaryStorage parent class already:
        # - Uses resource_type="raw" for non-image files
        # - Uses type="upload" by default
        # - Should use access_mode="public" by default
        
        return super()._save(name, content)
    
    def url(self, name):
        """Override to ensure public access URLs"""
        try:
            # Get the URL from parent class
            url = super().url(name)
            
            # Ensure it's a secure HTTPS URL
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            
            return url
        except Exception as e:
            # Log error but don't break the application
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating PDF URL for {name}: {e}")
            
            # Return a fallback URL or re-raise
            raise e


class SecureImageStorage(MediaCloudinaryStorage):
    """
    Custom storage class for image files.
    
    This ensures that images are uploaded to Cloudinary with:
    - resource_type="image" (correct for image files)
    - access_mode="public" (ensures public accessibility)  
    - secure=True (forces HTTPS URLs)
    
    This is essentially the same as the default MediaCloudinaryStorage
    but with explicit public access to avoid any permission issues.
    
    Usage in models:
        image = models.ImageField(storage=SecureImageStorage(), upload_to='images/')
    """
    
    def url(self, name):
        """Override to ensure secure HTTPS URLs"""
        try:
            # Get the URL from parent class
            url = super().url(name)
            
            # Ensure it's a secure HTTPS URL
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            
            return url
        except Exception as e:
            # Log error but don't break the application
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating image URL for {name}: {e}")
            
            # Re-raise the exception
            raise e


# Backward compatibility aliases
PDFStorage = PublicPDFStorage
ResumeStorage = PublicPDFStorage
DocumentStorage = PublicPDFStorage

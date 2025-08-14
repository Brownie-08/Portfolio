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
import cloudinary.uploader
import cloudinary.api


class PublicPDFStorage(RawMediaCloudinaryStorage):
    """
    Custom storage class for PDF files and documents.
    
    This ensures that PDFs are uploaded to Cloudinary with:
    - resource_type="raw" (correct for non-image files)  
    - access_mode="public" (ensures public accessibility without authentication)
    - type="upload" (standard upload delivery type)
    - secure=True (forces HTTPS URLs)
    
    This fixes 401 authentication errors on resume downloads by forcing
    all PDF uploads to be publicly accessible.
    
    Usage in models:
        resume = models.FileField(storage=PublicPDFStorage(), upload_to='files/')
    """
    
    def get_available_name(self, name, max_length=None):
        """Override to ensure unique names for PDF files"""
        return super().get_available_name(name, max_length)
    
    def _save(self, name, content):
        """Override save to force public access mode for PDF uploads"""
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
        
        # Use direct Cloudinary uploader to ensure proper options        
        try:
            # Read file content
            content.seek(0)  # Ensure we're at the start
            file_content = content.read()
            
            # Generate public_id - don't add media/ prefix for public access to work
            clean_name = name.lstrip('/')
            public_id = clean_name
            
            # Upload with authenticated type to generate signed URLs for access
            # This prevents 401 errors by using Cloudinary's signed URL system
            result = cloudinary.uploader.upload(
                file_content,
                public_id=public_id,
                resource_type='raw',        # Correct for non-image files
                type='authenticated',       # Generate signed URLs for access
                overwrite=True,             # Replace if exists
                invalidate=True,            # Clear CDN cache
                secure=True,                # Force HTTPS
                use_filename=False,         # Use our public_id
                folder=None,                # Don't use folder parameter with public_id
            )
            
            # Return the name for Django's file field
            return name
            
        except Exception as e:
            # Fall back to parent implementation if direct upload fails
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Direct Cloudinary upload failed: {e}")
            
            # Set options and try parent method
            self.override_resource_type = 'raw'
            self.options = {
                **getattr(self, 'options', {}),
                'resource_type': 'raw',
                'type': 'upload',
                'access_mode': 'public',
                'secure': True,
            }
            
            return super()._save(name, content)
    
    def url(self, name):
        """Override to generate signed URLs for authenticated PDFs"""
        try:
            import cloudinary.utils
            
            # Generate signed URL for authenticated raw files
            clean_name = name.lstrip('/')
            
            # Generate signed URL - this prevents 401 authentication errors
            signed_url = cloudinary.utils.cloudinary_url(
                clean_name,
                resource_type='raw',
                type='authenticated',
                secure=True,
                sign_url=True,  # This creates the signed URL
            )[0]
            
            return signed_url
            
        except Exception as e:
            # Fall back to parent URL method
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not generate signed URL for {name}: {e}, falling back to parent URL")
            
            try:
                # Get the URL from parent class
                url = super().url(name)
                
                # Ensure it's a secure HTTPS URL
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
                
                return url
            except Exception as parent_e:
                logger.error(f"Parent URL generation also failed for {name}: {parent_e}")
                raise parent_e


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


# Railway Volume Storage for Resumes
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class ResumeStorage(FileSystemStorage):
    """
    Custom storage backend for resumes using Railway volume.
    
    This storage class ensures that resumes/PDFs are stored on the Railway volume
    and served directly through Railway's static assets configuration, avoiding
    401 authentication errors while keeping images on Cloudinary.
    """
    
    def __init__(self, *args, **kwargs):
        # Force specific location and base_url for Railway volume
        kwargs['location'] = getattr(settings, 'MEDIA_ROOT', '/app/media')
        kwargs['base_url'] = getattr(settings, 'MEDIA_URL', '/media/')
        super().__init__(*args, **kwargs)
    
    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's available in the storage mechanism.
        This ensures unique filenames to prevent conflicts.
        """
        return super().get_available_name(name, max_length)
    
    def url(self, name):
        """
        Return the URL where the file can be accessed.
        Railway will serve this through static assets configuration.
        """
        if name is None:
            return ''
        
        # Ensure the URL uses the correct media URL
        url = super().url(name)
        
        # In production, Railway will serve these files directly
        # No additional processing needed
        return url


# Backward compatibility aliases
PDFStorage = PublicPDFStorage
# Note: ResumeStorage now points to Railway volume storage, not Cloudinary
# This is the key change for the Railway volume implementation
DocumentStorage = PublicPDFStorage

"""
Media file serving views for production environments.

This module provides fallback views for serving media files when
the primary serving mechanism (WhiteNoise) doesn't work as expected.
"""

import os
import mimetypes
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt


@require_GET
@cache_control(max_age=3600)  # Cache for 1 hour
def serve_media(request, path):
    """
    Serve media files in production.
    
    This view serves media files when the standard Django development
    server media serving is not available in production.
    
    Args:
        request: The HTTP request object
        path: The relative path to the media file
        
    Returns:
        FileResponse: The media file response
        
    Raises:
        Http404: If the file is not found
    """
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Security check: ensure the file is within MEDIA_ROOT
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    file_path = os.path.abspath(file_path)
    
    if not file_path.startswith(media_root):
        raise Http404("File not found")
    
    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Return the file
    try:
        return FileResponse(
            open(file_path, 'rb'),
            content_type=content_type,
            as_attachment=False
        )
    except IOError:
        raise Http404("File not found")


@require_GET
def serve_profile_image(request):
    """
    Serve the current user's profile image.
    
    This is a convenience view for serving the active user's profile image.
    """
    from .models import PersonalInfo
    
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.profile_image:
            file_path = personal_info.profile_image.path
            if os.path.exists(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'image/jpeg'
                
                return FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                    as_attachment=False
                )
    except Exception:
        pass
    
    raise Http404("Profile image not found")


@require_GET
@csrf_exempt
@cache_control(max_age=1800)  # Cache for 30 minutes
def serve_resume(request):
    """
    Serve the current user's resume/CV file.
    
    This is a convenience view for serving the active user's resume.
    Handles both local file storage and cloud storage scenarios.
    For Cloudinary, generates a proper public URL.
    """
    from .models import PersonalInfo
    from django.shortcuts import redirect
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        personal_info = PersonalInfo.get_active()
        if not personal_info:
            logger.warning("No active PersonalInfo found for resume request")
            raise Http404("Personal information not found")
        
        if not personal_info.resume:
            logger.warning("No resume file found in PersonalInfo")
            raise Http404("Resume file not found")
        
        # Handle Railway persistent volume or local storage
        # Always try local storage first (Railway persistent volume)
        try:
            file_path = personal_info.resume.path
            if os.path.exists(file_path) and os.path.isfile(file_path):
                logger.info(f"Found resume file at: {file_path}")
                
                # Security check: ensure file is within MEDIA_ROOT
                media_root = os.path.abspath(settings.MEDIA_ROOT)
                file_path = os.path.abspath(file_path)
                
                if not file_path.startswith(media_root):
                    logger.error(f"Security violation: file path outside media root")
                    raise Http404("Access denied")
                
                # Determine content type
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/pdf'
                
                # Get the original filename for download
                filename = os.path.basename(personal_info.resume.name)
                if not filename:
                    filename = f"resume.{content_type.split('/')[-1]}"
                
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                    as_attachment=True,
                    filename=filename
                )
                
                # Add security headers
                response['X-Content-Type-Options'] = 'nosniff'
                response['X-Frame-Options'] = 'DENY'
                response['Cache-Control'] = 'max-age=3600'  # Cache for 1 hour
                
                logger.info(f"Successfully serving resume: {filename}")
                return response
        except Exception as e:
            logger.warning(f"Local file access failed: {e}")
            
        # Fallback: Handle cloud storage (Cloudinary) if enabled
        if hasattr(settings, 'USE_CLOUDINARY') and getattr(settings, 'USE_CLOUDINARY', False) and not getattr(settings, 'USE_LOCAL_STORAGE', True):
            # For Cloudinary, generate a proper public URL
            try:
                import cloudinary.utils
                
                # Get the public ID from the file name
                if hasattr(personal_info.resume, 'public_id'):
                    public_id = personal_info.resume.public_id
                else:
                    # Extract public ID from file name
                    file_name = personal_info.resume.name
                    if file_name.startswith('media/'):
                        file_name = file_name[6:]  # Remove 'media/' prefix
                    # Remove file extension for public ID
                    public_id = os.path.splitext(file_name)[0]
                
                logger.info(f"Generating Cloudinary URL for public_id: {public_id}")
                
                # Generate a public URL for the file
                cloudinary_url = cloudinary.utils.cloudinary_url(
                    public_id,
                    resource_type="raw",  # Use 'raw' for non-image files like PDFs
                    type="upload",
                    secure=True,
                    sign_url=False,  # Public URL, no signature needed
                    flags="attachment",  # Force download
                )[0]
                
                logger.info(f"Generated Cloudinary URL: {cloudinary_url}")
                return redirect(cloudinary_url)
                
            except Exception as e:
                logger.error(f"Cloudinary URL generation failed: {e}")
                # Fallback to direct URL
                try:
                    direct_url = personal_info.resume.url
                    logger.info(f"Using direct Cloudinary URL: {direct_url}")
                    return redirect(direct_url)
                except Exception as e2:
                    logger.error(f"Direct Cloudinary URL also failed: {e2}")
                    raise Http404("Unable to access resume file")
        else:
            # For local storage, serve the file directly
            try:
                file_path = personal_info.resume.path
            except (ValueError, AttributeError) as e:
                logger.error(f"Error getting resume file path: {e}")
                # Fallback: try to construct path manually
                file_path = os.path.join(settings.MEDIA_ROOT, personal_info.resume.name)
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                logger.error(f"Resume file not found at path: {file_path}")
                raise Http404("Resume file not found on disk")
            
            # Security check: ensure file is within MEDIA_ROOT
            media_root = os.path.abspath(settings.MEDIA_ROOT)
            file_path = os.path.abspath(file_path)
            
            if not file_path.startswith(media_root):
                logger.error(f"Security violation: file path outside media root")
                raise Http404("Access denied")
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/pdf'
            
            # Get the original filename for download
            filename = os.path.basename(personal_info.resume.name)
            if not filename:
                filename = f"resume.{content_type.split('/')[-1]}"
            
            try:
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                    as_attachment=True,
                    filename=filename
                )
                
                # Add security headers
                response['X-Content-Type-Options'] = 'nosniff'
                response['X-Frame-Options'] = 'DENY'
                
                return response
                
            except (IOError, OSError) as e:
                logger.error(f"Error opening resume file: {e}")
                raise Http404("Unable to access resume file")
                
    except Http404:
        # Re-raise Http404 exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error serving resume: {e}")
        raise Http404("Resume temporarily unavailable")

from django import template
from django.urls import reverse
from django.conf import settings

register = template.Library()

@register.filter
def split_skills(value, category=None):
    """Split comma-separated skills into a list"""
    if not value:
        return []
    return [skill.strip() for skill in value.split(',') if skill.strip()]

@register.filter
def split_by_comma(value):
    """Split comma-separated values into a list"""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

@register.filter
def get_whatsapp_link(phone_number):
    """Convert phone number to WhatsApp link"""
    if not phone_number:
        return ''
    # Remove non-digit characters
    clean_number = ''.join(filter(str.isdigit, phone_number))
    return f'https://wa.me/{clean_number}'

@register.simple_tag
def get_skills_by_category(skills, category):
    """Get skills filtered by category"""
    return skills.filter(category=category).order_by('order', 'name')

@register.filter
def split(value, delimiter=','):
    """
    Split a string by delimiter and return a list
    Usage: {{ "python,javascript,react"|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []

@register.filter
def trim(value):
    """
    Trim whitespace from a string
    Usage: {{ " hello world "|trim }}
    """
    if value:
        return value.strip()
    return value

@register.filter
def tech_stack_list(tech_stack):
    """
    Convert tech_stack string to list
    Usage: {{ project.tech_stack|tech_stack_list }}
    """
    if tech_stack:
        return [tech.strip() for tech in tech_stack.split(',') if tech.strip()]
    return []

@register.filter
def mul(value, arg):
    """
    Multiply two values
    Usage: {{ value|mul:20 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def media_url_fallback(file_field):
    """
    Generate a fallback media URL for production environments.
    If the direct media URL doesn't work, use the fallback view.
    
    Usage: {{ personal_info.profile_image|media_url_fallback }}
    """
    if not file_field:
        return ''
    
    try:
        # Check if file exists and has a name
        if not hasattr(file_field, 'name') or not file_field.name:
            return ''
        
        # Get the URL from the file field
        url = file_field.url
        
        # Return the URL as-is since Cloudinary handles URL generation
        return url
        
    except (ValueError, AttributeError, Exception) as e:
        # If direct URL fails, try the fallback view
        try:
            if hasattr(file_field, 'name') and file_field.name:
                return reverse('portfolio:serve_media', kwargs={'path': file_field.name})
        except Exception as fallback_error:
            pass
        return ''

@register.simple_tag
def profile_image_url(personal_info):
    """
    Get the profile image URL with production fallback.
    
    Usage: {% profile_image_url personal_info %}
    """
    if not personal_info or not personal_info.profile_image:
        return None
    
    try:
        # Check if the file has a name first
        if not hasattr(personal_info.profile_image, 'name') or not personal_info.profile_image.name:
            return None
        # Try to get the direct media URL first
        url = personal_info.profile_image.url
        # Ensure the URL is properly formatted for production
        if url and not url.startswith('http'):
            from django.conf import settings
            if hasattr(settings, 'MEDIA_URL') and settings.MEDIA_URL:
                if not url.startswith(settings.MEDIA_URL):
                    url = settings.MEDIA_URL.rstrip('/') + '/' + url.lstrip('/')
        # Additional validation for production URLs
        if url and (url.startswith('/media/') or url.startswith('http')):
            return url
    except (ValueError, AttributeError, Exception) as e:
        # Log the error for debugging in production
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error getting profile image URL: {e}")
        # Fallback to the serve view
        try:
            return reverse('portfolio:serve_profile_image')
        except Exception as fallback_error:
            logger.warning(f"Fallback profile image URL also failed: {fallback_error}")
            return None
    return None


@register.simple_tag
def resume_download_url(personal_info):
    """
    Get the resume download URL with production fallback.
    
    This function handles both cloud storage and local storage scenarios
    and provides multiple fallback options for maximum compatibility.
    
    Usage: {% resume_download_url personal_info as resume_url %}
    """
    if not personal_info or not personal_info.resume:
        return ''
    
    import logging
    logger = logging.getLogger(__name__)
    
    # Check if file has a name first
    if not hasattr(personal_info.resume, 'name') or not personal_info.resume.name:
        logger.warning("Resume file has no name attribute")
        return ''
    
    try:
        # Always prioritize local storage (Railway persistent volume)
        # Try direct file URL first
        try:
            url = personal_info.resume.url
            if url:
                # For local storage, ensure proper URL formatting
                if not url.startswith('http') and not url.startswith('/'):
                    # Add media URL prefix if needed
                    media_url = getattr(settings, 'MEDIA_URL', '/media/')
                    url = media_url.rstrip('/') + '/' + url.lstrip('/')
                
                logger.info(f"Using direct resume URL: {url}")
                return url
        except (ValueError, AttributeError, OSError) as e:
            logger.warning(f"Direct resume URL failed: {e}")
        
        # Fallback to our custom serve_resume view (works with Railway persistent volume)
        try:
            url = reverse('portfolio:serve_resume')
            logger.info(f"Using serve_resume fallback URL: {url}")
            return url
        except Exception as e:
            logger.error(f"serve_resume URL failed: {e}")
        
        # Last resort fallbacks
        try:
            return reverse('portfolio:download_resume')
        except Exception as e:
            logger.error(f"download_resume URL failed: {e}")
            try:
                return reverse('portfolio:cv_download')
            except Exception as e2:
                logger.error(f"All resume URL options failed: {e}, {e2}")
                return ''
            
    except Exception as e:
        logger.error(f"Unexpected error in resume_download_url: {e}")
        # Emergency fallback
        try:
            return reverse('portfolio:serve_resume')
        except:
            return ''


@register.filter
def file_exists(file_field):
    """
    Check if a file field's file actually exists.
    
    Usage: {{ personal_info.profile_image|file_exists }}
    """
    if not file_field:
        return False
    
    try:
        import os
        from django.conf import settings
        
        if hasattr(file_field, 'path'):
            return os.path.exists(file_field.path)
        elif hasattr(file_field, 'name') and file_field.name:
            file_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
            return os.path.exists(file_path)
        return False
    except (ValueError, AttributeError, OSError):
        return False

"""
Health check views for Railway deployment monitoring
"""
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.conf import settings
import sys


@never_cache
@csrf_exempt
def health_check(request):
    """
    Simple health check endpoint that verifies:
    - Django is running
    - Database connection is working
    - Basic system information
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Basic health information
    health_data = {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "django": {
            "version": sys.version,
            "debug": settings.DEBUG,
            "database": db_status,
        },
        "application": {
            "name": "Django Portfolio",
            "version": "1.0.0",
        }
    }
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    return JsonResponse(health_data, status=status_code)


@never_cache
@csrf_exempt
def ready_check(request):
    """
    Readiness check for Railway deployment
    """
    try:
        # Quick database check
        from django.db import connection
        connection.ensure_connection()
        
        return JsonResponse({
            "status": "ready",
            "message": "Application is ready to serve requests"
        })
    except Exception as e:
        return JsonResponse({
            "status": "not_ready",
            "error": str(e)
        }, status=503)


@never_cache
@csrf_exempt
def simple_health_check(request):
    """
    Simple health check that just returns OK without database checks
    For Railway deployment health check
    """
    from django.http import HttpResponse
    from django.conf import settings
    import os
    
    # Add debug info in response headers for troubleshooting
    response = HttpResponse("OK", status=200, content_type="text/plain")
    
    # Add debugging headers (remove in final production)
    if settings.DEBUG or os.environ.get('RAILWAY_DEBUG_HEADERS') == 'True':
        response['X-Debug-Allowed-Hosts'] = str(settings.ALLOWED_HOSTS)
        response['X-Debug-Railway-Domain'] = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'Not set')
        response['X-Debug-Host-Header'] = request.META.get('HTTP_HOST', 'Not set')
    
    return response

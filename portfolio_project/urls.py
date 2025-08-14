"""
URL configuration for portfolio_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio.health import health_check, ready_check, simple_health_check
from portfolio.views import healthz, health_simple, railway_status

urlpatterns = [
    # Health check endpoints for Railway
    path('health/', health_check, name='health_check'),
    path('ready/', ready_check, name='ready_check'),
    path('healthz/', simple_health_check, name='healthz'),  # Simple health check for Railway
    
    # Main application URLs
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('portfolio.urls')),
]

# Media files handling:
# - Development: Django serves from local MEDIA_ROOT
# - Production: Railway static assets serve from volume + Cloudinary for images

if settings.DEBUG:
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug Toolbar URLs (development only)
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

# Static files - always include for fallback
# WhiteNoise middleware handles this in production, but include as fallback
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
from portfolio.health import health_check, ready_check

urlpatterns = [
    # Health check endpoints for Railway
    path('health/', health_check, name='health_check'),
    path('ready/', ready_check, name='ready_check'),
    path('healthz/', health_check, name='healthz'),  # Alternative endpoint
    
    # Main application URLs
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('portfolio.urls')),
]

# Serve media files - different handling for development vs production
if settings.DEBUG:
    # In development, serve media files directly
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In production, still serve media files if using local storage as fallback
    # This is handled by WhiteNoise middleware or cloud storage
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files - always include for fallback
# WhiteNoise middleware should handle this in production, but include as fallback
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug Toolbar URLs (development only)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

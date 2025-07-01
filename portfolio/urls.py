from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Projects URLs
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Contact page
    path('contact/', views.contact, name='contact'),
]

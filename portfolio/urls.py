from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # About page
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Projects URLs
    path('projects/', views.ProjectListView.as_view(), name='projects_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Blog URLs
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Contact page
    path('contact/', views.ContactView.as_view(), name='contact'),
]

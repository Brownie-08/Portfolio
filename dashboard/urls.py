from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Dashboard URLs
    path('', views.DashboardHomeView.as_view(), name='home'),
    
    # Personal Information URLs
    path('personal-info/', views.EnhancedPersonalInfoUpdateView.as_view(), name='personal_info'),
    path('upload-cv/', views.UploadCVView.as_view(), name='upload_cv'),
    
    # Project Management URLs
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Blog Management URLs
    path('blog/', views.BlogPostListView.as_view(), name='blog_posts'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_delete'),
    
    # Education Management URLs
    path('education/', views.EducationListView.as_view(), name='education'),
    path('education/create/', views.EducationCreateView.as_view(), name='education_create'),
    path('education/<int:pk>/edit/', views.EducationUpdateView.as_view(), name='education_edit'),
    path('education/<int:pk>/delete/', views.EducationDeleteView.as_view(), name='education_delete'),
    
    # Certification Management URLs
    path('certifications/', views.CertificationListView.as_view(), name='certifications'),
    path('certifications/create/', views.CertificationCreateView.as_view(), name='certification_create'),
    path('certifications/<int:pk>/edit/', views.CertificationUpdateView.as_view(), name='certification_edit'),
    path('certifications/<int:pk>/delete/', views.CertificationDeleteView.as_view(), name='certification_delete'),
    
    # Award Management URLs
    path('awards/', views.AwardListView.as_view(), name='awards'),
    path('awards/create/', views.AwardCreateView.as_view(), name='award_create'),
    path('awards/<int:pk>/edit/', views.AwardUpdateView.as_view(), name='award_edit'),
    path('awards/<int:pk>/delete/', views.AwardDeleteView.as_view(), name='award_delete'),
    
    # SEO Management URLs
    path('seo/', views.SEOListView.as_view(), name='seo'),
    path('seo/create/', views.SEOCreateView.as_view(), name='seo_create'),
    path('seo/<int:pk>/edit/', views.SEOUpdateView.as_view(), name='seo_edit'),
    path('seo/<int:pk>/delete/', views.SEODeleteView.as_view(), name='seo_delete'),
    
    # Testimonial Management URLs
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonials'),
    path('testimonials/create/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),
    
    # Skills Management URLs
    path('skills/', views.SkillListView.as_view(), name='skills'),
    path('skills/create/', views.SkillCreateView.as_view(), name='skill_create'),
    path('skills/<int:pk>/edit/', views.SkillUpdateView.as_view(), name='skill_edit'),
    path('skills/<int:pk>/delete/', views.SkillDeleteView.as_view(), name='skill_delete'),
    
    # Career Timeline Management URLs
    path('career/', views.CareerTimelineListView.as_view(), name='career'),
    path('career/create/', views.CareerTimelineCreateView.as_view(), name='career_create'),
    path('career/<int:pk>/edit/', views.CareerTimelineUpdateView.as_view(), name='career_edit'),
    path('career/<int:pk>/delete/', views.CareerTimelineDeleteView.as_view(), name='career_delete'),
    
    # Footer Links Management URLs
    path('footer-links/', views.FooterLinkListView.as_view(), name='footer_links'),
    path('footer-links/create/', views.FooterLinkCreateView.as_view(), name='footer_link_create'),
    path('footer-links/<int:pk>/edit/', views.FooterLinkUpdateView.as_view(), name='footer_link_edit'),
    path('footer-links/<int:pk>/delete/', views.FooterLinkDeleteView.as_view(), name='footer_link_delete'),
    
    # Contact Messages
    path('messages/', views.ContactMessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/', views.ContactMessageDetailView.as_view(), name='message_detail'),
]

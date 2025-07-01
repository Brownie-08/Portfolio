from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    PersonalInfo, Skill, Project, Testimonial, 
    Experience, Education, BlogPost, ContactMessage
)
from .forms import ContactForm


class HomeView(TemplateView):
    """Home page view with personal info, featured projects, and skills"""
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal information
        context['personal_info'] = PersonalInfo.objects.first()
        
        # Get featured projects (limit to 3)
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        
        # Get featured skills grouped by category
        context['featured_skills'] = Skill.objects.filter(is_featured=True).order_by('category', '-proficiency')
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        
        # Get latest blog posts if any
        context['latest_blog_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        
        return context


class AboutView(TemplateView):
    """About page with detailed personal info, experience, education, and skills"""
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal information
        context['personal_info'] = PersonalInfo.objects.first()
        
        # Get work experience
        context['experiences'] = Experience.objects.all()
        
        # Get education
        context['education'] = Education.objects.all()
        
        # Get all skills grouped by category
        skills_by_category = {}
        for skill in Skill.objects.all():
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        context['skills_by_category'] = skills_by_category
        
        # Get all testimonials
        context['testimonials'] = Testimonial.objects.all()
        
        return context


class ProjectsListView(ListView):
    """Projects listing page"""
    model = Project
    template_name = 'portfolio/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(technologies__name__icontains=search_query)
            ).distinct()
        
        # Filter by technology
        technology = self.request.GET.get('technology')
        if technology:
            queryset = queryset.filter(technologies__name__iexact=technology)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all technologies for filtering
        context['technologies'] = Skill.objects.filter(
            project__isnull=False
        ).distinct().order_by('name')
        
        # Get project statuses for filtering
        context['statuses'] = Project.PROJECT_STATUS
        
        # Pass current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_technology'] = self.request.GET.get('technology', '')
        context['current_status'] = self.request.GET.get('status', '')
        
        return context


class ProjectDetailView(DetailView):
    """Individual project detail page"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related projects (same technologies or featured)
        current_project = self.object
        related_projects = Project.objects.filter(
            Q(technologies__in=current_project.technologies.all()) |
            Q(is_featured=True)
        ).exclude(id=current_project.id).distinct()[:3]
        
        context['related_projects'] = related_projects
        
        return context


class BlogListView(ListView):
    """Blog posts listing page"""
    model = BlogPost
    template_name = 'portfolio/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all tags for filtering
        all_posts = BlogPost.objects.filter(is_published=True)
        all_tags = set()
        for post in all_posts:
            if post.tags:
                all_tags.update(post.tags)
        context['all_tags'] = sorted(all_tags)
        
        # Get featured posts
        context['featured_posts'] = BlogPost.objects.filter(
            is_published=True, is_featured=True
        )[:3]
        
        # Pass current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        
        return context


class BlogDetailView(DetailView):
    """Individual blog post detail page"""
    model = BlogPost
    template_name = 'portfolio/blog_detail.html'
    context_object_name = 'blog_post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related posts (same tags or featured)
        current_post = self.object
        related_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=current_post.id)
        
        # Try to find posts with similar tags
        if current_post.tags:
            for tag in current_post.tags:
                related_posts = related_posts.filter(tags__icontains=tag)
                if related_posts.exists():
                    break
        
        # If no related posts found, get featured posts
        if not related_posts.exists():
            related_posts = BlogPost.objects.filter(
                is_published=True, is_featured=True
            ).exclude(id=current_post.id)
        
        context['related_posts'] = related_posts[:3]
        
        return context


class ContactView(FormView):
    """Contact page with form submission"""
    template_name = 'portfolio/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('portfolio:contact')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal information for contact details
        context['personal_info'] = PersonalInfo.objects.first()
        
        return context
    
    def form_valid(self, form):
        # Save the contact message
        contact_message = form.save()

        # Send email notification
        self.send_email_notification(contact_message)
        
        # Add success message
        messages.success(
            self.request, 
            'Thank you for your message! I will get back to you soon.'
        )
        
        return super().form_valid(form)
    
    def send_email_notification(self, contact_message):
        """Send email notification when a new contact message is received"""
        try:
            # Get contact email from settings
            contact_email = getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)
            admin_subject_prefix = getattr(settings, 'ADMIN_EMAIL_SUBJECT_PREFIX', '[Portfolio Contact] ')
            
            # Email to admin/owner
            admin_subject = f"{admin_subject_prefix}{contact_message.subject}"
            
            admin_message = f"""
New Contact Form Submission
============================

From: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}
Submitted: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Message:
{'-' * 40}
{contact_message.message}
{'-' * 40}

You can reply directly to {contact_message.email}

---
This message was sent from your portfolio website contact form.
            """
            
            # Send email to admin
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_email],
                fail_silently=False,
            )
            
            # Send auto-reply if enabled
            if getattr(settings, 'SEND_AUTO_REPLY', True):
                self.send_auto_reply(contact_message)
                
        except Exception as e:
            # Log the error but don't prevent form submission
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Email notification failed: {e}")
            print(f"Email notification failed: {e}")
    
    def send_auto_reply(self, contact_message):
        """Send an automatic reply to the contact form sender"""
        try:
            auto_reply_subject = "Thank you for contacting me!"
            
            auto_reply_message = f"""
Hi {contact_message.name},

Thank you for reaching out through my portfolio website! 

I have received your message about "{contact_message.subject}" and will get back to you as soon as possible, typically within 24-48 hours.

Here's a copy of your message for your records:
{'-' * 40}
{contact_message.message}
{'-' * 40}

If you have any urgent inquiries, please feel free to reach out to me directly.

Best regards,
Your Portfolio Owner

---
This is an automated response. Please do not reply to this email.
            """
            
            send_mail(
                subject=auto_reply_subject,
                message=auto_reply_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_message.email],
                fail_silently=True,  # Don't fail if auto-reply doesn't work
            )
            
        except Exception as e:
            # Log but don't fail the main process
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Auto-reply email failed: {e}")
    
    def form_invalid(self, form):
        # Add error message
        messages.error(
            self.request,
            'There was an error with your submission. Please check the form and try again.'
        )
        
        return super().form_invalid(form)


# Legacy function-based view names for backward compatibility
# These will call the class-based views
home = HomeView.as_view()
about = AboutView.as_view()
projects_list = ProjectsListView.as_view()
project_detail = ProjectDetailView.as_view()
blog_list = BlogListView.as_view()
blog_detail = BlogDetailView.as_view()
contact = ContactView.as_view()

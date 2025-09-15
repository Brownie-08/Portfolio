from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Tag, Project, Testimonial, 
    BlogPost, ContactMessage, PersonalInfo, Education, Certification, Award,
    Skill, CareerTimeline, FooterLink
)
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods


class HomeView(TemplateView):
    """Home page view with featured projects and testimonials"""
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured projects (limit to 3)
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.all()[:3]
        
        # Get latest blog posts if any
        context['latest_blog_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        
        return context


class AboutView(TemplateView):
    """About page with enhanced dynamic content"""
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal information
        context['personal_info'] = PersonalInfo.get_active()
        
        # Get all skills grouped by category
        context['skills'] = Skill.objects.all()
        context['skills_by_category'] = {}
        for choice in Skill.SKILL_CATEGORIES:
            category_key = choice[0]
            category_name = choice[1]
            skills = Skill.objects.filter(category=category_key).order_by('order', 'name')
            if skills.exists():
                context['skills_by_category'][category_name] = skills
        
        # Get career timeline
        context['career_timeline'] = CareerTimeline.objects.all()
        
        # Get featured testimonials
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)
        
        # Get all education entries
        context['educations'] = Education.objects.all()
        
        # Get featured certifications
        context['certifications'] = Certification.objects.filter(is_featured=True)
        
        # Get featured awards
        context['awards'] = Award.objects.filter(is_featured=True)
        
        return context


class ProjectListView(ListView):
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
                Q(tech_stack__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name__iexact=tag)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all tags for filtering
        context['tags'] = Tag.objects.all().order_by('name')
        
        # Get featured projects for the featured section
        context['featured_projects'] = Project.objects.filter(is_featured=True)
        
        # Pass current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        
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
        
        # Get related projects (same tags or featured)
        current_project = self.object
        related_projects = Project.objects.filter(
            Q(tags__in=current_project.tags.all()) |
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
                Q(body__icontains=search_query) |
                Q(excerpt__icontains=search_query)
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
                # Split comma-separated tags
                post_tags = [tag.strip() for tag in post.tags.split(',') if tag.strip()]
                all_tags.update(post_tags)
        context['all_tags'] = sorted(all_tags)
        
        # Get featured post (single)
        context['featured_post'] = BlogPost.objects.filter(
            is_published=True, is_featured=True
        ).first()
        
        # Note: blog_posts context is already provided by ListView
        
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
            post_tags = [tag.strip() for tag in current_post.tags.split(',') if tag.strip()]
            for tag in post_tags:
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
            
            # Get personal info for professional signature
            from .models import PersonalInfo
            personal_info = PersonalInfo.get_active()
            
            # Email to admin/owner
            admin_subject = f"{admin_subject_prefix}{contact_message.subject}"
            
            # Professional email template
            website_info = f"\n🌐 Website: {personal_info.website_url}" if personal_info and personal_info.website_url else ""
            location_info = f"\n📍 Location: {personal_info.location}" if personal_info and personal_info.location else ""
            
            admin_message = f"""
📧 NEW PORTFOLIO CONTACT SUBMISSION
{'=' * 50}

👤 CONTACT DETAILS:
Name: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}
Submitted: {contact_message.created.strftime('%B %d, %Y at %I:%M %p')}

💬 MESSAGE:
{'-' * 50}
{contact_message.message}
{'-' * 50}

🔄 NEXT STEPS:
• Reply directly to: {contact_message.email}
• View in dashboard: http://127.0.0.1:8000/dashboard/messages/
• Mark as read after responding

{'=' * 50}
🏷️ PORTFOLIO INFORMATION:
Owner: {personal_info.full_name if personal_info else 'Portfolio Owner'}
Portfolio: {personal_info.portfolio_name if personal_info else 'My Portfolio'}{website_info}{location_info}

---
⚡ This notification was automatically generated from your portfolio contact form.
📱 You can manage all messages from your dashboard.
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
            # Get personal info for professional signature
            from .models import PersonalInfo
            personal_info = PersonalInfo.get_active()
            
            # Professional auto-reply subject
            portfolio_name = personal_info.portfolio_name if personal_info else "My Portfolio"
            auto_reply_subject = f"Thank you for contacting {portfolio_name}!"
            
            # Professional auto-reply template
            full_name = personal_info.full_name if personal_info else "Portfolio Owner"
            current_role = f"\n{personal_info.current_role}" if personal_info and personal_info.current_role else ""
            email_contact = f"\n📧 Email: {personal_info.email}" if personal_info and personal_info.email else ""
            phone_contact = f"\n📞 Phone: {personal_info.phone}" if personal_info and personal_info.phone else ""
            website_link = f"\n🌐 Portfolio: {personal_info.website_url}" if personal_info and personal_info.website_url else ""
            linkedin_link = f"\n💼 LinkedIn: {personal_info.linkedin_url}" if personal_info and personal_info.linkedin_url else ""
            
            auto_reply_message = f"""
Hello {contact_message.name},

✨ Thank you for reaching out through my portfolio website!

I have successfully received your message regarding "{contact_message.subject}" and truly appreciate you taking the time to contact me.

📋 MESSAGE CONFIRMATION:
Your inquiry has been logged and I will respond personally within 24-48 hours. Here's a copy of your message for your records:

{'-' * 50}
{contact_message.message}
{'-' * 50}

🚀 WHAT'S NEXT:
• I'll review your message carefully
• You'll receive a personalized response soon
• Feel free to follow up if you have additional questions

📞 FOR URGENT MATTERS:
If you have time-sensitive inquiries, please don't hesitate to reach out directly using the contact information below.

{'=' * 50}
🏷️ CONTACT INFORMATION:
{full_name}{current_role}{email_contact}{phone_contact}{website_link}{linkedin_link}

Best regards,
{full_name}
{portfolio_name}

---
🤖 This is an automated confirmation. Please do not reply to this email.
💬 I'll be in touch with you personally very soon!
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


# Resume serving views for Railway production
# These work regardless of DEBUG setting and Railway configuration
from django.http import FileResponse, Http404
import os

def latest_resume_view(request):
    """
    Open the latest resume in the browser if supported (PDF viewer).
    Works with both Cloudinary and local storage.
    """
    from django.shortcuts import redirect
    
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.resume:
            # Check if the resume URL contains cloudinary - indicating Cloudinary storage
            resume_url = personal_info.resume.url
            
            if 'cloudinary' in resume_url.lower():
                # For Cloudinary storage, redirect to the direct URL
                return redirect(resume_url)
            else:
                # For local storage, serve the file directly
                try:
                    if hasattr(personal_info.resume, 'path') and os.path.exists(personal_info.resume.path):
                        response = FileResponse(
                            open(personal_info.resume.path, 'rb'), 
                            as_attachment=False,  # Open in browser
                            content_type='application/pdf'
                        )
                        # Add cache headers for better performance
                        response['Cache-Control'] = 'public, max-age=3600'
                        return response
                    else:
                        # Fallback - redirect to the URL anyway
                        return redirect(resume_url)
                except (AttributeError, OSError):
                    # If path doesn't exist, try redirecting to URL
                    return redirect(resume_url)
    except Exception as e:
        # Log error but don't expose details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error serving resume for viewing: {e}")
    
    raise Http404("Resume not found")

def latest_resume_download(request):
    """
    Force download of the latest resume.
    Works with both Cloudinary and local storage.
    """
    from django.shortcuts import redirect
    from django.http import HttpResponse
    
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.resume:
            # Check if the resume URL contains cloudinary - indicating Cloudinary storage
            resume_url = personal_info.resume.url
            
            if 'cloudinary' in resume_url.lower():
                # For Cloudinary storage, redirect to the direct URL with download parameters
                # Add download parameter to force download
                if '?' in resume_url:
                    url = resume_url + '&fl_attachment'
                else:
                    url = resume_url + '?fl_attachment'
                return redirect(url)
            else:
                # For local storage, serve the file directly
                try:
                    if hasattr(personal_info.resume, 'path') and os.path.exists(personal_info.resume.path):
                        filename = os.path.basename(personal_info.resume.name)
                        if not filename:
                            filename = "resume.pdf"
                        
                        response = FileResponse(
                            open(personal_info.resume.path, 'rb'), 
                            as_attachment=True,  # Force download
                            filename=filename,
                            content_type='application/pdf'
                        )
                        # Add cache headers for better performance
                        response['Cache-Control'] = 'public, max-age=3600'
                        return response
                    else:
                        # Fallback - redirect to the URL with download parameter
                        if '?' in resume_url:
                            url = resume_url + '&download=1'
                        else:
                            url = resume_url + '?download=1'
                        return redirect(url)
                except (AttributeError, OSError):
                    # If path doesn't exist, try redirecting to URL with download parameter
                    if '?' in resume_url:
                        url = resume_url + '&download=1'
                    else:
                        url = resume_url + '?download=1'
                    return redirect(url)
    except Exception as e:
        # Log error but don't expose details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error serving resume for download: {e}")
    
    raise Http404("Resume not found")


def resume_media_redirect(request, filename):
    """
    Redirect legacy /media/resumes/ URLs to the proper resume view.
    This eliminates 404 warnings for direct media URL access.
    """
    from django.shortcuts import redirect
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"Redirecting legacy media URL for: {filename}")
    
    # Redirect to the latest resume download view
    return redirect('portfolio:latest_resume_download')


# Legacy function-based view names for backward compatibility
# These will call the class-based views
home = HomeView.as_view()
about = AboutView.as_view()
projects_list = ProjectListView.as_view()
project_detail = ProjectDetailView.as_view()
blog_list = BlogListView.as_view()
blog_detail = BlogDetailView.as_view()
contact = ContactView.as_view()


# ============================================================================
# RAILWAY HEALTHCHECK ENDPOINTS - Bulletproof for production deployment
# ============================================================================

@never_cache
@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def healthz(request):
    """Railway-specific healthcheck endpoint that bypasses all Django restrictions.
    
    This endpoint is designed to always return 200 OK for Railway health checks,
    regardless of DEBUG settings, ALLOWED_HOSTS, or CSRF configuration.
    """
    return JsonResponse({"status": "ok"})


@never_cache
@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def health_simple(request):
    """Alternative simple health check - returns plain text OK.
    
    Backup healthcheck endpoint in case JSON response has issues.
    Railway can use either /healthz/ or /health-simple/ 
    """
    return HttpResponse("OK", content_type="text/plain", status=200)


@never_cache
@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def railway_status(request):
    """Railway deployment status check with minimal Django dependencies.
    
    Returns basic app status without database or complex operations.
    Use this as Railway healthcheck if others fail.
    """
    import os
    import django
    
    status_data = {
        "status": "healthy",
        "service": "django-portfolio",
        "django_version": django.get_version(),
        "debug_mode": settings.DEBUG,
        "environment": "railway-production",
        "timestamp": "",
    }
    
    try:
        from datetime import datetime
        status_data["timestamp"] = datetime.now().isoformat()
    except Exception:
        status_data["timestamp"] = "unknown"
    
    return JsonResponse(status_data)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from portfolio.models import (
    PersonalInfo, Project, BlogPost, ContactMessage, Education, 
    Certification, Award, SEOSettings, Testimonial, Skill, CareerTimeline, FooterLink
)
from .forms import (
    CustomLoginForm, EnhancedPersonalInfoForm, ProjectForm, BlogPostForm, CVUploadForm,
    EducationForm, CertificationForm, AwardForm, SEOForm, TestimonialForm,
    SkillForm, CareerTimelineForm, FooterLinkForm
)


class CustomLoginView(LoginView):
    """Custom login view with styled form"""
    form_class = CustomLoginForm
    template_name = 'dashboard/auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Dashboard home with overview statistics"""
    template_name = 'dashboard/home.html'
    login_url = reverse_lazy('dashboard:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        context['stats'] = {
            'total_projects': Project.objects.count(),
            'featured_projects': Project.objects.filter(is_featured=True).count(),
            'total_blog_posts': BlogPost.objects.count(),
            'published_posts': BlogPost.objects.filter(is_published=True).count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'recent_messages': ContactMessage.objects.filter(
                created__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
        
        # Recent activity
        context['recent_projects'] = Project.objects.order_by('-created_at')[:3]
        context['recent_posts'] = BlogPost.objects.order_by('-created')[:3]
        context['recent_messages'] = ContactMessage.objects.order_by('-created')[:5]
        
        return context


# This view is deprecated - use EnhancedPersonalInfoUpdateView instead
# class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
#     """Update personal information"""
#     model = PersonalInfo
#     form_class = EnhancedPersonalInfoForm  # Updated to use enhanced form
#     template_name = 'dashboard/personal_info.html'
#     success_url = reverse_lazy('dashboard:personal_info')
#     login_url = reverse_lazy('dashboard:login')
#     
#     def get_object(self):
#         # Get or create personal info for the current user
#         personal_info, created = PersonalInfo.objects.get_or_create(
#             is_active=True,
#             defaults={'full_name': self.request.user.get_full_name() or self.request.user.username}
#         )
#         return personal_info
#     
#     def form_valid(self, form):
#         messages.success(self.request, 'Personal information updated successfully!')
#         return super().form_valid(form)


class UploadCVView(LoginRequiredMixin, UpdateView):
    """Upload CV/Resume"""
    model = PersonalInfo
    form_class = CVUploadForm
    template_name = 'dashboard/upload_cv.html'
    success_url = reverse_lazy('dashboard:personal_info')
    login_url = reverse_lazy('dashboard:login')
    
    def get_object(self):
        personal_info, created = PersonalInfo.objects.get_or_create(
            is_active=True,
            defaults={'full_name': self.request.user.get_full_name() or self.request.user.username}
        )
        return personal_info
    
    def form_valid(self, form):
        messages.success(self.request, 'CV/Resume uploaded successfully!')
        return super().form_valid(form)


# Project Management Views
class ProjectListView(LoginRequiredMixin, ListView):
    """List all projects with management options"""
    model = Project
    template_name = 'dashboard/projects/list.html'
    context_object_name = 'projects'
    paginate_by = 10
    login_url = reverse_lazy('dashboard:login')
    
    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create new project"""
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/projects/form.html'
    success_url = reverse_lazy('dashboard:projects')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/projects/form.html'
    success_url = reverse_lazy('dashboard:projects')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    model = Project
    template_name = 'dashboard/projects/delete.html'
    success_url = reverse_lazy('dashboard:projects')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project deleted successfully!')
        return super().form_valid(form)


# Blog Management Views
class BlogPostListView(LoginRequiredMixin, ListView):
    """List all blog posts with management options"""
    model = BlogPost
    template_name = 'dashboard/blog/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    login_url = reverse_lazy('dashboard:login')
    
    def get_queryset(self):
        queryset = BlogPost.objects.all().order_by('-created')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        return queryset


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Create new blog post"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/blog/form.html'
    success_url = reverse_lazy('dashboard:blog_posts')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing blog post"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/blog/form.html'
    success_url = reverse_lazy('dashboard:blog_posts')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete blog post"""
    model = BlogPost
    template_name = 'dashboard/blog/delete.html'
    success_url = reverse_lazy('dashboard:blog_posts')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post deleted successfully!')
        return super().form_valid(form)


# Contact Message Views
class ContactMessageListView(LoginRequiredMixin, ListView):
    """List all contact messages with enhanced management"""
    model = ContactMessage
    template_name = 'dashboard/messages/list.html'
    context_object_name = 'messages'
    paginate_by = 20
    login_url = reverse_lazy('dashboard:login')
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all().order_by('-created')
        
        # Filter by read/unread status
        status = self.request.GET.get('status')
        if status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif status == 'read':
            queryset = queryset.filter(is_read=True)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(subject__icontains=search) |
                Q(message__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_messages'] = ContactMessage.objects.count()
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        context['current_status'] = self.request.GET.get('status', '')
        context['current_search'] = self.request.GET.get('search', '')
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle bulk actions"""
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_messages')
        
        if not selected_ids:
            messages.warning(request, 'No messages selected.')
            return redirect('dashboard:messages')
        
        if action == 'mark_read':
            ContactMessage.objects.filter(id__in=selected_ids).update(is_read=True)
            messages.success(request, f'{len(selected_ids)} messages marked as read.')
        elif action == 'mark_unread':
            ContactMessage.objects.filter(id__in=selected_ids).update(is_read=False)
            messages.success(request, f'{len(selected_ids)} messages marked as unread.')
        elif action == 'delete':
            ContactMessage.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'{len(selected_ids)} messages deleted.')
        
        return redirect('dashboard:messages')


class ContactMessageDetailView(LoginRequiredMixin, DetailView):
    """View contact message details and mark as read"""
    model = ContactMessage
    template_name = 'dashboard/messages/detail.html'
    context_object_name = 'message'
    login_url = reverse_lazy('dashboard:login')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Mark as read when viewed
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj


# Enhanced Personal Info View
class EnhancedPersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    """Enhanced update personal information with About page content"""
    model = PersonalInfo
    form_class = EnhancedPersonalInfoForm
    template_name = 'dashboard/personal_info.html'
    success_url = reverse_lazy('dashboard:personal_info')
    login_url = reverse_lazy('dashboard:login')
    
    def get_object(self):
        personal_info, created = PersonalInfo.objects.get_or_create(
            is_active=True,
            defaults={'full_name': self.request.user.get_full_name() or self.request.user.username}
        )
        return personal_info
    
    def form_valid(self, form):
        messages.success(self.request, 'Personal information updated successfully!')
        return super().form_valid(form)


# Education Management Views
class EducationListView(LoginRequiredMixin, ListView):
    """List all education entries"""
    model = Education
    template_name = 'dashboard/education/list.html'
    context_object_name = 'educations'
    login_url = reverse_lazy('dashboard:login')


class EducationCreateView(LoginRequiredMixin, CreateView):
    """Create new education entry"""
    model = Education
    form_class = EducationForm
    template_name = 'dashboard/education/form.html'
    success_url = reverse_lazy('dashboard:education')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education entry created successfully!')
        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing education entry"""
    model = Education
    form_class = EducationForm
    template_name = 'dashboard/education/form.html'
    success_url = reverse_lazy('dashboard:education')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education entry updated successfully!')
        return super().form_valid(form)


class EducationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete education entry"""
    model = Education
    template_name = 'dashboard/education/delete.html'
    success_url = reverse_lazy('dashboard:education')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education entry deleted successfully!')
        return super().form_valid(form)


# Certification Management Views
class CertificationListView(LoginRequiredMixin, ListView):
    """List all certifications"""
    model = Certification
    template_name = 'dashboard/certifications/list.html'
    context_object_name = 'certifications'
    login_url = reverse_lazy('dashboard:login')


class CertificationCreateView(LoginRequiredMixin, CreateView):
    """Create new certification"""
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/certifications/form.html'
    success_url = reverse_lazy('dashboard:certifications')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification created successfully!')
        return super().form_valid(form)


class CertificationUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing certification"""
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/certifications/form.html'
    success_url = reverse_lazy('dashboard:certifications')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully!')
        return super().form_valid(form)


class CertificationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete certification"""
    model = Certification
    template_name = 'dashboard/certifications/delete.html'
    success_url = reverse_lazy('dashboard:certifications')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification deleted successfully!')
        return super().form_valid(form)


# Award Management Views
class AwardListView(LoginRequiredMixin, ListView):
    """List all awards"""
    model = Award
    template_name = 'dashboard/awards/list.html'
    context_object_name = 'awards'
    login_url = reverse_lazy('dashboard:login')


class AwardCreateView(LoginRequiredMixin, CreateView):
    """Create new award"""
    model = Award
    form_class = AwardForm
    template_name = 'dashboard/awards/form.html'
    success_url = reverse_lazy('dashboard:awards')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Award created successfully!')
        return super().form_valid(form)


class AwardUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing award"""
    model = Award
    form_class = AwardForm
    template_name = 'dashboard/awards/form.html'
    success_url = reverse_lazy('dashboard:awards')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Award updated successfully!')
        return super().form_valid(form)


class AwardDeleteView(LoginRequiredMixin, DeleteView):
    """Delete award"""
    model = Award
    template_name = 'dashboard/awards/delete.html'
    success_url = reverse_lazy('dashboard:awards')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Award deleted successfully!')
        return super().form_valid(form)


# SEO Management Views
class SEOListView(LoginRequiredMixin, ListView):
    """List all SEO settings"""
    model = SEOSettings
    template_name = 'dashboard/seo/list.html'
    context_object_name = 'seo_settings'
    login_url = reverse_lazy('dashboard:login')


class SEOCreateView(LoginRequiredMixin, CreateView):
    """Create new SEO settings"""
    model = SEOSettings
    form_class = SEOForm
    template_name = 'dashboard/seo/form.html'
    success_url = reverse_lazy('dashboard:seo')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'SEO settings created successfully!')
        return super().form_valid(form)


class SEOUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing SEO settings"""
    model = SEOSettings
    form_class = SEOForm
    template_name = 'dashboard/seo/form.html'
    success_url = reverse_lazy('dashboard:seo')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'SEO settings updated successfully!')
        return super().form_valid(form)


class SEODeleteView(LoginRequiredMixin, DeleteView):
    """Delete SEO settings"""
    model = SEOSettings
    template_name = 'dashboard/seo/delete.html'
    success_url = reverse_lazy('dashboard:seo')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'SEO settings deleted successfully!')
        return super().form_valid(form)


# Testimonial Management Views
class TestimonialListView(LoginRequiredMixin, ListView):
    """List all testimonials"""
    model = Testimonial
    template_name = 'dashboard/testimonials/list.html'
    context_object_name = 'testimonials'
    login_url = reverse_lazy('dashboard:login')


class TestimonialCreateView(LoginRequiredMixin, CreateView):
    """Create new testimonial"""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonials/form.html'
    success_url = reverse_lazy('dashboard:testimonials')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Testimonial created successfully!')
        return super().form_valid(form)


class TestimonialUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing testimonial"""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonials/form.html'
    success_url = reverse_lazy('dashboard:testimonials')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Testimonial updated successfully!')
        return super().form_valid(form)


class TestimonialDeleteView(LoginRequiredMixin, DeleteView):
    """Delete testimonial"""
    model = Testimonial
    template_name = 'dashboard/testimonials/delete.html'
    success_url = reverse_lazy('dashboard:testimonials')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Testimonial deleted successfully!')
        return super().form_valid(form)


# Skill Management Views
class SkillListView(LoginRequiredMixin, ListView):
    """List all skills grouped by category"""
    model = Skill
    template_name = 'dashboard/skills/list.html'
    context_object_name = 'skills'
    login_url = reverse_lazy('dashboard:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group skills by category
        context['skills_by_category'] = {}
        for choice in Skill.SKILL_CATEGORIES:
            category_key = choice[0]
            category_name = choice[1]
            skills = Skill.objects.filter(category=category_key).order_by('order', 'name')
            if skills.exists():
                context['skills_by_category'][category_name] = skills
        return context


class SkillCreateView(LoginRequiredMixin, CreateView):
    """Create new skill"""
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/skills/form.html'
    success_url = reverse_lazy('dashboard:skills')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill created successfully!')
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing skill"""
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/skills/form.html'
    success_url = reverse_lazy('dashboard:skills')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill updated successfully!')
        return super().form_valid(form)


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    """Delete skill"""
    model = Skill
    template_name = 'dashboard/skills/delete.html'
    success_url = reverse_lazy('dashboard:skills')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill deleted successfully!')
        return super().form_valid(form)


# Career Timeline Management Views
class CareerTimelineListView(LoginRequiredMixin, ListView):
    """List all career timeline entries"""
    model = CareerTimeline
    template_name = 'dashboard/career/list.html'
    context_object_name = 'career_entries'
    login_url = reverse_lazy('dashboard:login')


class CareerTimelineCreateView(LoginRequiredMixin, CreateView):
    """Create new career timeline entry"""
    model = CareerTimeline
    form_class = CareerTimelineForm
    template_name = 'dashboard/career/form.html'
    success_url = reverse_lazy('dashboard:career')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Career entry created successfully!')
        return super().form_valid(form)


class CareerTimelineUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing career timeline entry"""
    model = CareerTimeline
    form_class = CareerTimelineForm
    template_name = 'dashboard/career/form.html'
    success_url = reverse_lazy('dashboard:career')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Career entry updated successfully!')
        return super().form_valid(form)


class CareerTimelineDeleteView(LoginRequiredMixin, DeleteView):
    """Delete career timeline entry"""
    model = CareerTimeline
    template_name = 'dashboard/career/delete.html'
    success_url = reverse_lazy('dashboard:career')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Career entry deleted successfully!')
        return super().form_valid(form)


# Footer Link Management Views
class FooterLinkListView(LoginRequiredMixin, ListView):
    """List all footer links grouped by category"""
    model = FooterLink
    template_name = 'dashboard/footer/list.html'
    context_object_name = 'footer_links'
    login_url = reverse_lazy('dashboard:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group links by category
        context['links_by_category'] = {}
        for choice in FooterLink.LINK_CATEGORIES:
            category_key = choice[0]
            category_name = choice[1]
            links = FooterLink.objects.filter(category=category_key, is_active=True).order_by('order', 'title')
            if links.exists():
                context['links_by_category'][category_name] = links
        return context


class FooterLinkCreateView(LoginRequiredMixin, CreateView):
    """Create new footer link"""
    model = FooterLink
    form_class = FooterLinkForm
    template_name = 'dashboard/footer/form.html'
    success_url = reverse_lazy('dashboard:footer_links')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Footer link created successfully!')
        return super().form_valid(form)


class FooterLinkUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing footer link"""
    model = FooterLink
    form_class = FooterLinkForm
    template_name = 'dashboard/footer/form.html'
    success_url = reverse_lazy('dashboard:footer_links')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Footer link updated successfully!')
        return super().form_valid(form)


class FooterLinkDeleteView(LoginRequiredMixin, DeleteView):
    """Delete footer link"""
    model = FooterLink
    template_name = 'dashboard/footer/delete.html'
    success_url = reverse_lazy('dashboard:footer_links')
    login_url = reverse_lazy('dashboard:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Footer link deleted successfully!')
        return super().form_valid(form)

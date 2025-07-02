from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import (
    Tag, Project, Testimonial, 
    ContactMessage, BlogPost
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_count']
    search_fields = ['name']
    ordering = ['name']
    
    def project_count(self, obj):
        """Display number of projects using this tag"""
        count = obj.project_set.count()
        if count > 0:
            url = reverse('admin:portfolio_project_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} project{}</a>', 
                             url, count, 's' if count != 1 else '')
        return '0 projects'
    project_count.short_description = 'Projects'
    project_count.admin_order_field = 'project_count'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'title', 'is_featured', 'tech_stack_display', 'created_at']
    list_filter = ['is_featured', 'tags', 'created_at']
    search_fields = ['title', 'description', 'tech_stack']
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    actions = ['mark_as_featured', 'unmark_as_featured']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Basic Information', {
            'fields': [('title', 'slug'), 'description', 'tech_stack']
        }),
        ('Media', {
            'fields': ['image', 'image_preview']
        }),
        ('Links', {
            'fields': [('live_url', 'repo_url')]
        }),
        ('Details', {
            'fields': ['tags', 'is_featured']
        })
    ]
    readonly_fields = ['created_at', 'image_preview']
    
    def image_thumbnail(self, obj):
        """Display small thumbnail in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return 'No image'
    image_thumbnail.short_description = 'Image'
    
    def image_preview(self, obj):
        """Display larger image preview in detail view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return 'No image uploaded'
    image_preview.short_description = 'Image Preview'
    
    def tech_stack_display(self, obj):
        """Display truncated tech stack"""
        if len(obj.tech_stack) > 50:
            return obj.tech_stack[:50] + '...'
        return obj.tech_stack
    tech_stack_display.short_description = 'Tech Stack'
    
    def mark_as_featured(self, request, queryset):
        """Custom action to mark projects as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} project{"s" if updated != 1 else ""} marked as featured.'
        )
    mark_as_featured.short_description = 'Mark selected projects as featured'
    
    def unmark_as_featured(self, request, queryset):
        """Custom action to unmark projects as featured"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{updated} project{"s" if updated != 1 else ""} unmarked as featured.'
        )
    unmark_as_featured.short_description = 'Unmark selected projects as featured'
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created_at'])
        return readonly


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['avatar_thumbnail', 'name', 'role', 'is_featured', 'created']
    list_filter = ['is_featured', 'created']
    search_fields = ['name', 'role', 'comment']
    list_editable = ['is_featured']
    actions = ['mark_as_featured', 'unmark_as_featured']
    date_hierarchy = 'created'
    fields = [
        ('name', 'role'),
        'comment',
        ('avatar', 'avatar_preview'),
        'is_featured'
    ]
    readonly_fields = ['created', 'avatar_preview']
    
    def avatar_thumbnail(self, obj):
        """Display small avatar thumbnail in list view"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;" />',
                obj.avatar.url
            )
        return 'No avatar'
    avatar_thumbnail.short_description = 'Avatar'
    
    def avatar_preview(self, obj):
        """Display larger avatar preview in detail view"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 8px;" />',
                obj.avatar.url
            )
        return 'No avatar uploaded'
    avatar_preview.short_description = 'Avatar Preview'
    
    def mark_as_featured(self, request, queryset):
        """Custom action to mark testimonials as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} testimonial{"s" if updated != 1 else ""} marked as featured.'
        )
    mark_as_featured.short_description = 'Mark selected testimonials as featured'
    
    def unmark_as_featured(self, request, queryset):
        """Custom action to unmark testimonials as featured"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{updated} testimonial{"s" if updated != 1 else ""} unmarked as featured.'
        )
    unmark_as_featured.short_description = 'Unmark selected testimonials as featured'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created']
    list_filter = ['is_read', 'created']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    actions = ['mark_as_read', 'mark_as_unread']
    date_hierarchy = 'created'
    readonly_fields = ['name', 'email', 'subject', 'message', 'created']
    fields = [
        ('name', 'email'),
        'subject',
        'message',
        'is_read',
        'created'
    ]
    
    def mark_as_read(self, request, queryset):
        """Custom action to mark messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(
            request,
            f'{updated} message{"s" if updated != 1 else ""} marked as read.'
        )
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_unread(self, request, queryset):
        """Custom action to mark messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(
            request,
            f'{updated} message{"s" if updated != 1 else ""} marked as unread.'
        )
    mark_as_unread.short_description = 'Mark selected messages as unread'
    
    def has_add_permission(self, request):
        # Contact messages should only be created through the contact form
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'title', 'excerpt_preview', 'is_published', 'created', 'updated']
    list_filter = ['is_published', 'created', 'updated']
    search_fields = ['title', 'body', 'excerpt']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['publish_posts', 'unpublish_posts']
    date_hierarchy = 'created'
    fieldsets = [
        ('Content', {
            'fields': [('title', 'slug'), 'excerpt', 'body']
        }),
        ('Media', {
            'fields': ['image', 'image_preview']
        }),
        ('Metadata', {
            'fields': ['is_published']
        })
    ]
    readonly_fields = ['created', 'updated', 'image_preview']
    
    def image_thumbnail(self, obj):
        """Display small thumbnail in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return 'No image'
    image_thumbnail.short_description = 'Image'
    
    def image_preview(self, obj):
        """Display larger image preview in detail view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return 'No image uploaded'
    image_preview.short_description = 'Image Preview'
    
    def excerpt_preview(self, obj):
        """Display truncated excerpt"""
        if obj.excerpt:
            if len(obj.excerpt) > 50:
                return obj.excerpt[:50] + '...'
            return obj.excerpt
        return 'No excerpt'
    excerpt_preview.short_description = 'Excerpt'
    
    def publish_posts(self, request, queryset):
        """Custom action to publish blog posts"""
        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            f'{updated} blog post{"s" if updated != 1 else ""} published.'
        )
    publish_posts.short_description = 'Publish selected blog posts'
    
    def unpublish_posts(self, request, queryset):
        """Custom action to unpublish blog posts"""
        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            f'{updated} blog post{"s" if updated != 1 else ""} unpublished.'
        )
    unpublish_posts.short_description = 'Unpublish selected blog posts'
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created', 'updated'])
        return readonly


# Customize admin site headers
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"

# Custom admin site configuration for grouping
class PortfolioAdminSite(admin.AdminSite):
    site_header = "Portfolio Content Management"
    site_title = "Portfolio CMS"
    index_title = "Content Administration"
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all installed apps with custom grouping.
        """
        app_dict = self._build_app_dict(request, app_label)
        
        # Custom grouping for portfolio models
        if 'portfolio' in app_dict:
            portfolio_models = app_dict['portfolio']['models']
            
            # Group models by category
            content_models = []
            communication_models = []
            
            for model in portfolio_models:
                model_name = model['object_name']
                if model_name in ['Project', 'BlogPost']:
                    content_models.append(model)
                elif model_name in ['Testimonial', 'ContactMessage']:
                    communication_models.append(model)
                else:  # Tag and other models
                    content_models.append(model)
            
            # Create grouped structure
            app_list = [
                {
                    'name': 'Content Management',
                    'app_label': 'content',
                    'models': content_models,
                    'app_url': '/admin/portfolio/',
                },
                {
                    'name': 'Communication',
                    'app_label': 'communication', 
                    'models': communication_models,
                    'app_url': '/admin/portfolio/',
                }
            ]
        else:
            app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
            
        return app_list

# Note: To use custom admin site, uncomment the following lines
# and update urls.py to use portfolio_admin_site instead of admin.site
# portfolio_admin_site = PortfolioAdminSite(name='portfolio_admin')
# portfolio_admin_site.register(Tag, TagAdmin)
# portfolio_admin_site.register(Project, ProjectAdmin)
# portfolio_admin_site.register(Testimonial, TestimonialAdmin)
# portfolio_admin_site.register(ContactMessage, ContactMessageAdmin)
# portfolio_admin_site.register(BlogPost, BlogPostAdmin)

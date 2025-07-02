from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Tag, Project, Testimonial, 
    ContactMessage, BlogPost
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'tags']
    search_fields = ['title', 'description', 'tech_stack']
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    fieldsets = [
        ('Basic Information', {
            'fields': [('title', 'slug'), 'description', 'tech_stack']
        }),
        ('Media', {
            'fields': ['image']
        }),
        ('Links', {
            'fields': [('live_url', 'repo_url')]
        }),
        ('Details', {
            'fields': ['tags', 'is_featured']
        })
    ]
    readonly_fields = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created_at'])
        return readonly


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'created']
    search_fields = ['name', 'role', 'comment']
    fields = [
        ('name', 'role'),
        'comment',
        'avatar'
    ]
    readonly_fields = ['created']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created']
    list_filter = ['is_read', 'created']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created']
    fields = [
        ('name', 'email'),
        'subject',
        'message',
        'is_read',
        'created'
    ]
    
    def has_add_permission(self, request):
        # Contact messages should only be created through the contact form
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created', 'updated']
    list_filter = ['is_published', 'created', 'updated']
    search_fields = ['title', 'body', 'excerpt']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Content', {
            'fields': [('title', 'slug'), 'excerpt', 'body']
        }),
        ('Media', {
            'fields': ['image']
        }),
        ('Metadata', {
            'fields': ['is_published']
        })
    ]
    readonly_fields = ['created', 'updated']
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created', 'updated'])
        return readonly


# Customize admin site headers
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"

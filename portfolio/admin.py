from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PersonalInfo, Skill, Project, Testimonial, 
    Experience, Education, ContactMessage, BlogPost
)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'updated_at']
    fields = [
        ('name', 'title'),
        'bio',
        ('email', 'phone'),
        'location',
        ('linkedin_url', 'github_url', 'twitter_url'),
        'resume_file',
        'profile_image',
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one PersonalInfo instance
        return not PersonalInfo.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['name']
    list_editable = ['proficiency', 'is_featured']
    ordering = ['-proficiency', 'name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'start_date', 'created_at']
    list_filter = ['status', 'is_featured', 'technologies']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'status']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    fieldsets = [
        ('Basic Information', {
            'fields': [('title', 'slug'), 'description', 'detailed_description']
        }),
        ('Media', {
            'fields': ['featured_image', 'gallery_images']
        }),
        ('Links', {
            'fields': [('live_url', 'github_url')]
        }),
        ('Details', {
            'fields': [
                'technologies', 'status', 
                ('start_date', 'end_date'),
                ('is_featured', 'order')
            ]
        })
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created_at', 'updated_at'])
        return readonly


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'position', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'company']
    search_fields = ['name', 'company', 'content']
    list_editable = ['is_featured', 'rating']
    fields = [
        ('name', 'position'),
        'company',
        'content',
        'image',
        ('rating', 'is_featured')
    ]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'technologies']
    search_fields = ['company', 'position', 'description']
    list_editable = ['is_current']
    filter_horizontal = ['technologies']
    fieldsets = [
        ('Basic Information', {
            'fields': [('company', 'position'), 'location', 'company_url']
        }),
        ('Duration', {
            'fields': [('start_date', 'end_date'), 'is_current']
        }),
        ('Details', {
            'fields': ['description', 'achievements', 'technologies', 'order']
        })
    ]
    ordering = ['-start_date']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date']
    search_fields = ['institution', 'degree', 'field_of_study']
    fields = [
        ('institution', 'institution_url'),
        ('degree', 'field_of_study'),
        ('start_date', 'end_date'),
        'gpa',
        'description',
        'achievements'
    ]
    ordering = ['-start_date']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    fields = [
        ('name', 'email'),
        'subject',
        'message',
        'is_read',
        'created_at'
    ]
    
    def has_add_permission(self, request):
        # Contact messages should only be created through the contact form
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'is_featured', 'published_at', 'created_at']
    list_filter = ['is_published', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Content', {
            'fields': [('title', 'slug'), 'excerpt', 'content']
        }),
        ('Media', {
            'fields': ['featured_image']
        }),
        ('Metadata', {
            'fields': ['tags', ('is_published', 'is_featured')]
        }),
        ('Timestamps', {
            'fields': ['published_at'],
            'classes': ['collapse']
        })
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['created_at', 'updated_at'])
        return readonly


# Customize admin site headers
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"

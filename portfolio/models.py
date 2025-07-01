from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


class PersonalInfo(models.Model):
    """Model for storing personal information that appears across the site"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    resume_file = models.FileField(upload_to='documents/', blank=True)
    profile_image = models.ImageField(upload_to='images/profile/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)


class Skill(models.Model):
    """Model for skills/technologies"""
    SKILL_CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.IntegerField(help_text="Proficiency level from 1-100")
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon (e.g., fab fa-python)")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-proficiency', 'name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Model for portfolio projects"""
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planning', 'Planning'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Skill, blank=True)
    featured_image = models.ImageField(upload_to='images/projects/')
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of additional image URLs")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.featured_image:
            img = Image.open(self.featured_image.path)
            if img.height > 800 or img.width > 1200:
                output_size = (1200, 800)
                img.thumbnail(output_size)
                img.save(self.featured_image.path)


class Testimonial(models.Model):
    """Model for client/colleague testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/testimonials/', blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"


class Experience(models.Model):
    """Model for work experience"""
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.JSONField(default=list, blank=True, help_text="List of key achievements")
    technologies = models.ManyToManyField(Skill, blank=True)
    company_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    """Model for education background"""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    achievements = models.JSONField(default=list, blank=True)
    institution_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class BlogPost(models.Model):
    """Optional blog post model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    featured_image = models.ImageField(upload_to='images/blog/', blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio:blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

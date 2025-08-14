from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Local storage for resume files (served directly by Railway/Django)
resume_storage = FileSystemStorage(
    location=getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media')),
    base_url=getattr(settings, 'MEDIA_URL', '/media/')
)


class Tag(models.Model):
    """Model for project tags"""
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated list of technologies")
    image = models.ImageField(upload_to='images/projects/', blank=True)
    live_url = models.URLField(blank=True, help_text="URL to live project")
    repo_url = models.URLField(blank=True, help_text="URL to repository")
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # GitHub integration fields
    github_repo = models.CharField(max_length=200, blank=True, 
                                 help_text="GitHub repository name (e.g., username/repo-name)")
    is_github_synced = models.BooleanField(default=False, 
                                         help_text="Automatically sync from GitHub")
    github_stars = models.IntegerField(default=0)
    github_forks = models.IntegerField(default=0)
    github_language = models.CharField(max_length=50, blank=True)
    github_updated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.title)[:40]
            if not base_slug:
                base_slug = str(uuid.uuid4())[:8]
            
            # Ensure unique slug
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})


class Testimonial(models.Model):
    """Model for client/colleague testimonials"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    comment = models.TextField()
    avatar = models.ImageField(upload_to='images/testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class BlogPost(models.Model):
    """Optional blog post model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='images/blog/', blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of tags")
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio:blog_detail', kwargs={'slug': self.slug})


class PersonalInfo(models.Model):
    """Model for personal information and branding"""
    portfolio_name = models.CharField(max_length=100, default="My Portfolio")
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField()
    location = models.CharField(max_length=100, blank=True, help_text="Your location (e.g., City, Country)")
    profile_image = models.ImageField(upload_to='images/profile/', blank=True)
    
    # About page specific fields
    about_intro = models.TextField(blank=True, help_text="Introduction paragraph for About page")
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of professional experience")
    current_role = models.CharField(max_length=200, blank=True, help_text="Current job title/role")
    professional_summary = models.TextField(blank=True, help_text="Professional journey summary")
    
    # Skills and interests
    technical_skills = models.TextField(blank=True, help_text="Comma-separated list of technical skills")
    soft_skills = models.TextField(blank=True, help_text="Comma-separated list of soft skills")
    interests = models.TextField(blank=True, help_text="Personal interests and hobbies")
    
    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Resume/CV - Uses local storage (served directly by Railway)
    resume = models.FileField(
        storage=resume_storage,
        upload_to='resumes/',
        blank=True,
        help_text="Upload your resume/CV (PDF, DOC, DOCX). Served directly from /media/ path."
    )
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description for homepage")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma-separated)")
    
    # Settings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
    
    def __str__(self):
        return f"{self.full_name} - {self.portfolio_name}"
    
    def save(self, *args, **kwargs):
        # Auto-delete old resume file when uploading a new one
        if self.pk:  # Only for existing objects (updates)
            try:
                old_instance = PersonalInfo.objects.get(pk=self.pk)
                if old_instance.resume and self.resume and old_instance.resume.name != self.resume.name:
                    # Delete old resume file from storage
                    import os
                    if hasattr(old_instance.resume, 'path') and os.path.isfile(old_instance.resume.path):
                        os.remove(old_instance.resume.path)
                    else:
                        # Try to delete using the storage backend
                        old_instance.resume.delete(save=False)
            except (PersonalInfo.DoesNotExist, ValueError, OSError) as e:
                # Log the error but don't prevent saving
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Could not delete old resume file: {e}")
        
        # Clear cache when personal info is updated
        cache.delete('personal_info')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active(cls):
        """Get the active personal info instance with caching"""
        info = cache.get('personal_info')
        if not info:
            info = cls.objects.filter(is_active=True).first()
            if info:
                cache.set('personal_info', info, 3600)  # Cache for 1 hour
        return info


class Education(models.Model):
    """Model for education details"""
    school_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, help_text="e.g., Bachelor of Science in Computer Science")
    field_of_study = models.CharField(max_length=200, blank=True, help_text="e.g., Computer Science")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if currently enrolled")
    grade = models.CharField(max_length=100, blank=True, help_text="e.g., First Class, 3.8 GPA")
    description = models.TextField(blank=True, help_text="Additional details about your education")
    location = models.CharField(max_length=200, blank=True)
    is_current = models.BooleanField(default=False, help_text="Currently enrolled")
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = first)")
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.school_name}"
    
    @property
    def duration(self):
        """Return formatted duration string"""
        start_year = self.start_date.year
        if self.is_current or not self.end_date:
            return f"{start_year} - Present"
        return f"{start_year} - {self.end_date.year}"


class Certification(models.Model):
    """Model for certifications and achievements"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True, help_text="Leave blank if no expiry")
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True, help_text="Link to verify certification")
    description = models.TextField(blank=True)
    certificate_image = models.ImageField(upload_to='images/certifications/', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"
    
    @property
    def is_expired(self):
        """Check if certification is expired"""
        if not self.expiry_date:
            return False
        return self.expiry_date < timezone.now().date()


class Award(models.Model):
    """Model for awards and recognitions"""
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    date_received = models.DateField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Academic, Professional, Community")
    award_image = models.ImageField(upload_to='images/awards/', blank=True)
    award_url = models.URLField(blank=True, help_text="Link to award details")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_received']
    
    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"


class SEOSettings(models.Model):
    """Model for managing SEO settings for different pages"""
    PAGE_CHOICES = [
        ('home', 'Homepage'),
        ('about', 'About Page'),
        ('projects', 'Projects Page'),
        ('blog', 'Blog Page'),
        ('contact', 'Contact Page'),
    ]
    
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=60, help_text="SEO title (60 chars max)")
    description = models.CharField(max_length=160, help_text="Meta description (160 chars max)")
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    og_title = models.CharField(max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.CharField(max_length=160, blank=True, help_text="Open Graph description")
    og_image = models.ImageField(upload_to='images/seo/', blank=True, help_text="Open Graph image")
    
    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"
    
    def __str__(self):
        return f"SEO - {self.get_page_display()}"


class Skill(models.Model):
    """Model for managing skills dynamically"""
    SKILL_CATEGORIES = [
        ('frontend', 'Front-End Development'),
        ('backend', 'Back-End Development'),
        ('tools', 'Tools & Technologies'),
        ('devops', 'DevOps & Cloud'),
        ('database', 'Database Technologies'),
        ('mobile', 'Mobile Development'),
        ('other', 'Other Skills'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.IntegerField(default=3, help_text="Skill level 1-5 (1=Beginner, 5=Expert)")
    description = models.TextField(blank=True, help_text="Optional description of your experience with this skill")
    icon_class = models.CharField(max_length=100, blank=True, help_text="CSS class for skill icon (e.g., fab fa-python)")
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")
    is_featured = models.BooleanField(default=False, help_text="Show prominently on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    @property
    def proficiency_stars(self):
        """Return HTML for star rating display"""
        stars = '★' * self.proficiency + '☆' * (5 - self.proficiency)
        return stars


class CareerTimeline(models.Model):
    """Model for professional journey/career timeline"""
    JOB_TYPES = [
        ('fulltime', 'Full-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
    ]
    
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_url = models.URLField(blank=True, help_text="Company website URL")
    location = models.CharField(max_length=200, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='fulltime')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current position")
    is_current = models.BooleanField(default=False, help_text="Currently working here")
    description = models.TextField(help_text="Describe your role, responsibilities, and achievements")
    technologies = models.TextField(blank=True, help_text="Technologies used (comma-separated)")
    achievements = models.TextField(blank=True, help_text="Key achievements and accomplishments")
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = most recent)")
    
    class Meta:
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"
    
    @property
    def duration(self):
        """Calculate and return formatted duration"""
        start_year = self.start_date.year
        start_month = self.start_date.month
        
        if self.is_current or not self.end_date:
            end_date = timezone.now().date()
            duration_str = f"{start_month:02d}/{start_year} - Present"
        else:
            end_date = self.end_date
            duration_str = f"{start_month:02d}/{start_year} - {self.end_date.month:02d}/{self.end_date.year}"
        
        # Calculate duration in months
        months = (end_date.year - start_year) * 12 + (end_date.month - start_month)
        years = months // 12
        remaining_months = months % 12
        
        if years > 0 and remaining_months > 0:
            duration_str += f" ({years}y {remaining_months}m)"
        elif years > 0:
            duration_str += f" ({years}y)"
        elif remaining_months > 0:
            duration_str += f" ({remaining_months}m)"
        
        return duration_str


class FooterLink(models.Model):
    """Model for managing footer quick links"""
    LINK_CATEGORIES = [
        ('quick', 'Quick Links'),
        ('services', 'Services'),
        ('resources', 'Resources'),
        ('social', 'Social Media'),
        ('legal', 'Legal'),
    ]
    
    title = models.CharField(max_length=100)
    url = models.URLField(help_text="Internal URL (e.g., /about/) or external URL (e.g., https://github.com)")
    category = models.CharField(max_length=20, choices=LINK_CATEGORIES, default='quick')
    icon_class = models.CharField(max_length=100, blank=True, help_text="CSS icon class (e.g., bi bi-house)")
    order = models.PositiveIntegerField(default=0)
    is_external = models.BooleanField(default=False, help_text="Opens in new tab")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

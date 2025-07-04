from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, Fieldset
from crispy_forms.bootstrap import PrependedText, AppendedText
from portfolio.models import (
    PersonalInfo, Project, BlogPost, Education, Certification, 
    Award, SEOSettings, Testimonial, Skill, CareerTimeline, FooterLink
)


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4"><h2 class="fw-bold text-primary">Dashboard Login</h2><p class="text-muted">Access your portfolio management dashboard</p></div>'),
            Field('username', placeholder='Username', css_class='form-control-lg'),
            Field('password', placeholder='Password', css_class='form-control-lg'),
            Div(
                Submit('submit', 'Login', css_class='btn btn-primary btn-lg w-100'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'portfolio_name', 'full_name', 'email', 'phone', 'bio', 'location',
            'profile_image', 'github_url', 'linkedin_url', 'twitter_url',
            'website_url', 'resume'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-person-circle me-2"></i>Personal Information</h3>'),
            Div(
                Div('portfolio_name', css_class='col-md-6'),
                Div('full_name', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('email', css_class='col-md-6'),
                Div('phone', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('location', css_class='col-md-12'),
                css_class='row'
            ),
            'bio',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-image me-2"></i>Profile Image</h4>'),
            'profile_image',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-link-45deg me-2"></i>Social Links</h4>'),
            Div(
                Div(PrependedText('github_url', '<i class="bi bi-github"></i>'), css_class='col-md-6'),
                Div(PrependedText('linkedin_url', '<i class="bi bi-linkedin"></i>'), css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div(PrependedText('twitter_url', '<i class="bi bi-twitter"></i>'), css_class='col-md-6'),
                Div(PrependedText('website_url', '<i class="bi bi-globe"></i>'), css_class='col-md-6'),
                css_class='row'
            ),
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-file-earmark-pdf me-2"></i>Resume/CV</h4>'),
            'resume',
            Div(
                Submit('submit', 'Update Personal Information', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'tech_stack', 'image', 'live_url', 
            'repo_url', 'is_featured', 'tags'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tech_stack': forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, React, PostgreSQL'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-folder-plus me-2"></i>Project Details</h3>'),
            'title',
            'description',
            'tech_stack',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-image me-2"></i>Project Image</h4>'),
            'image',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-link-45deg me-2"></i>Links</h4>'),
            Div(
                Div(PrependedText('live_url', '<i class="bi bi-globe"></i>'), css_class='col-md-6'),
                Div(PrependedText('repo_url', '<i class="bi bi-github"></i>'), css_class='col-md-6'),
                css_class='row'
            ),
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-gear me-2"></i>Settings</h4>'),
            Div(
                Div('is_featured', css_class='col-md-6'),
                Div('tags', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Save Project', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'body', 'image', 'tags', 
            'is_featured', 'is_published'
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3, 'maxlength': 300}),
            'body': forms.Textarea(attrs={'rows': 10}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g., Django, Web Development, Python'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-journal-plus me-2"></i>Blog Post Details</h3>'),
            'title',
            'excerpt',
            'body',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-image me-2"></i>Featured Image</h4>'),
            'image',
            HTML('<h4 class="mt-4 mb-3"><i class="bi bi-tags me-2"></i>Tags & Settings</h4>'),
            'tags',
            Div(
                Div('is_featured', css_class='col-md-6'),
                Div('is_published', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Save Blog Post', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class CVUploadForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-file-earmark-pdf me-2"></i>Upload CV/Resume</h3>'),
            HTML('<p class="text-muted mb-4">Upload your latest CV/Resume. Supported formats: PDF, DOC, DOCX</p>'),
            'resume',
            Div(
                Submit('submit', 'Upload CV', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class EnhancedPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'portfolio_name', 'full_name', 'email', 'phone', 'bio', 'location',
            'profile_image', 'about_intro', 'years_experience', 'current_role',
            'professional_summary', 'technical_skills', 'soft_skills', 'interests',
            'github_url', 'linkedin_url', 'twitter_url', 'website_url', 'instagram_url',
            'resume', 'meta_description', 'meta_keywords'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'about_intro': forms.Textarea(attrs={'rows': 4}),
            'professional_summary': forms.Textarea(attrs={'rows': 6}),
            'technical_skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, JavaScript, React, Docker, AWS'}),
            'soft_skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leadership, Communication, Problem Solving, Team Collaboration'}),
            'interests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Photography, Travel, Open Source, Technology Trends'}),
            'meta_description': forms.Textarea(attrs={'rows': 2, 'maxlength': 160}),
            'meta_keywords': forms.TextInput(attrs={'placeholder': 'web developer, django, python, portfolio'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                Div(
                    Div('portfolio_name', css_class='col-md-6'),
                    Div('full_name', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div('email', css_class='col-md-6'),
                    Div('phone', css_class='col-md-6'),
                    css_class='row'
                ),
                'location',
                'bio',
                'profile_image',
            ),
            Fieldset(
                'About Page Content',
                'about_intro',
                Div(
                    Div('years_experience', css_class='col-md-6'),
                    Div('current_role', css_class='col-md-6'),
                    css_class='row'
                ),
                'professional_summary',
            ),
            Fieldset(
                'Skills & Interests',
                'technical_skills',
                'soft_skills',
                'interests',
            ),
            Fieldset(
                'Social Links',
                Div(
                    Div(PrependedText('github_url', '<i class="bi bi-github"></i>'), css_class='col-md-6'),
                    Div(PrependedText('linkedin_url', '<i class="bi bi-linkedin"></i>'), css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div(PrependedText('twitter_url', '<i class="bi bi-twitter"></i>'), css_class='col-md-4'),
                    Div(PrependedText('website_url', '<i class="bi bi-globe"></i>'), css_class='col-md-4'),
                    Div(PrependedText('instagram_url', '<i class="bi bi-instagram"></i>'), css_class='col-md-4'),
                    css_class='row'
                ),
            ),
            Fieldset(
                'Resume & SEO',
                'resume',
                'meta_description',
                'meta_keywords',
            ),
            Div(
                Submit('submit', 'Update Information', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'school_name', 'degree', 'field_of_study', 'start_date', 'end_date',
            'grade', 'description', 'location', 'is_current', 'order'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-mortarboard me-2"></i>Education Details</h3>'),
            Div(
                Div('school_name', css_class='col-md-8'),
                Div('order', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('degree', css_class='col-md-6'),
                Div('field_of_study', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('start_date', css_class='col-md-4'),
                Div('end_date', css_class='col-md-4'),
                Div('is_current', css_class='col-md-4 d-flex align-items-end'),
                css_class='row'
            ),
            Div(
                Div('grade', css_class='col-md-6'),
                Div('location', css_class='col-md-6'),
                css_class='row'
            ),
            'description',
            Div(
                Submit('submit', 'Save Education', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            'name', 'issuing_organization', 'issue_date', 'expiry_date',
            'credential_id', 'credential_url', 'description', 'certificate_image',
            'is_featured', 'order'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-award me-2"></i>Certification Details</h3>'),
            Div(
                Div('name', css_class='col-md-8'),
                Div('order', css_class='col-md-4'),
                css_class='row'
            ),
            'issuing_organization',
            Div(
                Div('issue_date', css_class='col-md-6'),
                Div('expiry_date', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('credential_id', css_class='col-md-6'),
                Div('credential_url', css_class='col-md-6'),
                css_class='row'
            ),
            'description',
            'certificate_image',
            Div(
                Div('is_featured', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Save Certification', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = [
            'title', 'issuing_organization', 'date_received', 'description',
            'category', 'award_image', 'award_url', 'is_featured', 'order'
        ]
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-trophy me-2"></i>Award Details</h3>'),
            Div(
                Div('title', css_class='col-md-8'),
                Div('order', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('issuing_organization', css_class='col-md-6'),
                Div('date_received', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('category', css_class='col-md-6'),
                Div('award_url', css_class='col-md-6'),
                css_class='row'
            ),
            'description',
            'award_image',
            Div(
                Div('is_featured', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Save Award', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOSettings
        fields = [
            'page', 'title', 'description', 'keywords',
            'og_title', 'og_description', 'og_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'maxlength': 160}),
            'og_description': forms.Textarea(attrs={'rows': 3, 'maxlength': 160}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-search me-2"></i>SEO Settings</h3>'),
            'page',
            Div(
                Div('title', css_class='col-md-12'),
                css_class='row'
            ),
            'description',
            'keywords',
            HTML('<h4 class="mt-4 mb-3">Open Graph (Social Media)</h4>'),
            'og_title',
            'og_description',
            'og_image',
            Div(
                Submit('submit', 'Save SEO Settings', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'comment', 'avatar', 'is_featured']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-chat-quote me-2"></i>Testimonial Details</h3>'),
            Div(
                Div('name', css_class='col-md-6'),
                Div('role', css_class='col-md-6'),
                css_class='row'
            ),
            'comment',
            'avatar',
            'is_featured',
            Div(
                Submit('submit', 'Save Testimonial', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            'name', 'category', 'proficiency', 'description', 'icon_class',
            'order', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'proficiency': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-gear me-2"></i>Skill Details</h3>'),
            Div(
                Div('name', css_class='col-md-6'),
                Div('category', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('proficiency', css_class='col-md-4'),
                Div('order', css_class='col-md-4'),
                Div('is_featured', css_class='col-md-4 d-flex align-items-end'),
                css_class='row'
            ),
            'description',
            'icon_class',
            Div(
                Submit('submit', 'Save Skill', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class CareerTimelineForm(forms.ModelForm):
    class Meta:
        model = CareerTimeline
        fields = [
            'job_title', 'company', 'company_url', 'location', 'job_type',
            'start_date', 'end_date', 'is_current', 'description',
            'technologies', 'achievements', 'order'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'technologies': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, React, AWS, etc.'}),
            'achievements': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-briefcase me-2"></i>Career Timeline Entry</h3>'),
            Div(
                Div('job_title', css_class='col-md-8'),
                Div('order', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('company', css_class='col-md-6'),
                Div('company_url', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('location', css_class='col-md-6'),
                Div('job_type', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('start_date', css_class='col-md-4'),
                Div('end_date', css_class='col-md-4'),
                Div('is_current', css_class='col-md-4 d-flex align-items-end'),
                css_class='row'
            ),
            'description',
            'technologies',
            'achievements',
            Div(
                Submit('submit', 'Save Career Entry', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )


class FooterLinkForm(forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = [
            'title', 'url', 'category', 'icon_class', 'order',
            'is_external', 'is_active'
        ]
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': '/about/ or https://github.com/username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4"><i class="bi bi-link me-2"></i>Footer Link Details</h3>'),
            Div(
                Div('title', css_class='col-md-6'),
                Div('category', css_class='col-md-6'),
                css_class='row'
            ),
            'url',
            Div(
                Div('icon_class', css_class='col-md-6'),
                Div('order', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('is_external', css_class='col-md-6'),
                Div('is_active', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Save Footer Link', css_class='btn btn-primary btn-lg'),
                css_class='d-grid gap-2 mt-4'
            ),
        )

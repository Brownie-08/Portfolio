from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    PersonalInfo, Project, Skill, Education, Certification, Award,
    CareerTimeline, Testimonial, BlogPost, FooterLink, Tag
)
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seed production database with portfolio data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting production data seeding...'))

        # Create superuser if it doesn't exist
        self.create_superuser()
        
        # Seed personal info
        self.seed_personal_info()
        
        # Seed skills
        self.seed_skills()
        
        # Seed education
        self.seed_education()
        
        # Seed projects
        self.seed_projects()
        
        # Seed testimonials
        self.seed_testimonials()
        
        # Seed footer links
        self.seed_footer_links()
        
        # Seed blog posts
        self.seed_blog_posts()

        self.stdout.write(self.style.SUCCESS('✅ Production data seeding completed!'))

    def create_superuser(self):
        """Create a superuser for admin access"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@portfolio.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))
        else:
            self.stdout.write('Admin user already exists')

    def seed_personal_info(self):
        """Seed personal information"""
        personal_info, created = PersonalInfo.objects.get_or_create(
            id=1,
            defaults={
                'full_name': 'Peter E. Udoh',
                'portfolio_name': 'Peter Udoh Portfolio',
                'tagline': 'Full-Stack Developer & Tech Enthusiast',
                'bio': """I'm a passionate full-stack developer with expertise in Python, Django, 
                         JavaScript, and modern web technologies. I love creating efficient, 
                         scalable solutions and turning ideas into reality.""",
                'email': 'peter@example.com',
                'phone': '+1234567890',
                'location': 'Remote / Global',
                'linkedin_url': 'https://linkedin.com/in/peterudoh',
                'github_url': 'https://github.com/peterudoh',
                'twitter_url': 'https://twitter.com/peterudoh',
                'website_url': 'https://peterudoh.dev',
                'years_of_experience': 3,
                'clients_served': 15,
                'projects_completed': 25,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created personal info'))
        else:
            self.stdout.write('Personal info already exists')

    def seed_skills(self):
        """Seed skills data"""
        skills_data = [
            # Backend
            {'name': 'Python', 'category': 'backend', 'proficiency': 90, 'order': 1},
            {'name': 'Django', 'category': 'backend', 'proficiency': 85, 'order': 2},
            {'name': 'Django REST Framework', 'category': 'backend', 'proficiency': 80, 'order': 3},
            {'name': 'PostgreSQL', 'category': 'backend', 'proficiency': 75, 'order': 4},
            
            # Frontend
            {'name': 'JavaScript', 'category': 'frontend', 'proficiency': 80, 'order': 1},
            {'name': 'HTML5', 'category': 'frontend', 'proficiency': 90, 'order': 2},
            {'name': 'CSS3', 'category': 'frontend', 'proficiency': 85, 'order': 3},
            {'name': 'Bootstrap', 'category': 'frontend', 'proficiency': 80, 'order': 4},
            {'name': 'React', 'category': 'frontend', 'proficiency': 70, 'order': 5},
            
            # Tools
            {'name': 'Git', 'category': 'tools', 'proficiency': 85, 'order': 1},
            {'name': 'Docker', 'category': 'tools', 'proficiency': 70, 'order': 2},
            {'name': 'AWS', 'category': 'tools', 'proficiency': 65, 'order': 3},
            {'name': 'Railway', 'category': 'tools', 'proficiency': 75, 'order': 4},
        ]

        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(f'✅ Created skill: {skill.name}')

    def seed_education(self):
        """Seed education data"""
        education_data = [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Technology',
                'location': 'Tech City',
                'start_date': '2018-09-01',
                'end_date': '2022-06-01',
                'gpa': '3.8',
                'description': 'Focused on software engineering, algorithms, and web development.',
                'is_featured': True,
            }
        ]

        for edu_data in education_data:
            education, created = Education.objects.get_or_create(
                degree=edu_data['degree'],
                institution=edu_data['institution'],
                defaults=edu_data
            )
            if created:
                self.stdout.write(f'✅ Created education: {education.degree}')

    def seed_projects(self):
        """Seed project data"""
        projects_data = [
            {
                'title': 'E-Commerce Platform',
                'slug': 'e-commerce-platform',
                'description': 'Full-featured e-commerce platform built with Django and React',
                'long_description': 'A comprehensive e-commerce solution featuring user authentication, product management, shopping cart, payment processing, and admin dashboard.',
                'tech_stack': 'Django, React, PostgreSQL, Stripe API',
                'github_url': 'https://github.com/peterudoh/ecommerce-platform',
                'live_url': 'https://ecommerce-demo.com',
                'status': 'completed',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Task Management API',
                'slug': 'task-management-api',
                'description': 'RESTful API for task management with team collaboration features',
                'long_description': 'A robust API built with Django REST Framework featuring user management, project organization, task tracking, and real-time notifications.',
                'tech_stack': 'Django REST Framework, PostgreSQL, Redis, Celery',
                'github_url': 'https://github.com/peterudoh/task-api',
                'status': 'completed',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Portfolio Website',
                'slug': 'portfolio-website',
                'description': 'Personal portfolio website showcasing projects and skills',
                'long_description': 'A responsive portfolio website built with Django, featuring dynamic content management, contact forms, and admin interface.',
                'tech_stack': 'Django, Bootstrap, PostgreSQL, Railway',
                'github_url': 'https://github.com/peterudoh/portfolio',
                'live_url': 'https://peterudoh.dev',
                'status': 'completed',
                'is_featured': True,
                'order': 3,
            },
        ]

        # Create tags
        tags = ['Web Development', 'Django', 'React', 'API', 'E-commerce', 'Portfolio']
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )
            if created:
                # Add tags to project
                if 'Django' in project_data['tech_stack']:
                    django_tag = Tag.objects.get(name='Django')
                    project.tags.add(django_tag)
                
                web_dev_tag = Tag.objects.get(name='Web Development')
                project.tags.add(web_dev_tag)
                
                self.stdout.write(f'✅ Created project: {project.title}')

    def seed_testimonials(self):
        """Seed testimonial data"""
        testimonials_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_title': 'Product Manager',
                'client_company': 'TechStart Inc.',
                'testimonial': 'Peter delivered exceptional work on our e-commerce platform. His attention to detail and technical expertise made our project a success.',
                'rating': 5,
                'is_featured': True,
                'order': 1,
            },
            {
                'client_name': 'Mike Chen',
                'client_title': 'CTO',
                'client_company': 'InnovateLab',
                'testimonial': 'Working with Peter was a great experience. He understood our requirements perfectly and delivered a robust API solution.',
                'rating': 5,
                'is_featured': True,
                'order': 2,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                client_company=testimonial_data['client_company'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'✅ Created testimonial from: {testimonial.client_name}')

    def seed_footer_links(self):
        """Seed footer links"""
        footer_links_data = [
            {
                'title': 'LinkedIn',
                'url': 'https://linkedin.com/in/peterudoh',
                'category': 'social',
                'order': 1,
                'is_active': True,
            },
            {
                'title': 'GitHub',
                'url': 'https://github.com/peterudoh',
                'category': 'social',
                'order': 2,
                'is_active': True,
            },
            {
                'title': 'Twitter',
                'url': 'https://twitter.com/peterudoh',
                'category': 'social',
                'order': 3,
                'is_active': True,
            },
        ]

        for link_data in footer_links_data:
            link, created = FooterLink.objects.get_or_create(
                title=link_data['title'],
                defaults=link_data
            )
            if created:
                self.stdout.write(f'✅ Created footer link: {link.title}')

    def seed_blog_posts(self):
        """Seed blog posts"""
        blog_posts_data = [
            {
                'title': 'Getting Started with Django Development',
                'slug': 'getting-started-with-django',
                'excerpt': 'Learn the fundamentals of Django web development and build your first application.',
                'body': '''# Getting Started with Django Development

Django is a powerful Python web framework that makes it easy to build robust web applications. In this post, we'll cover the basics of getting started with Django development.

## What is Django?

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries included" philosophy, providing many built-in features.

## Key Features

- **ORM**: Object-Relational Mapping for database operations
- **Admin Interface**: Automatic admin interface for your models
- **URL Routing**: Clean and flexible URL design
- **Template System**: Powerful templating engine
- **Security**: Built-in protection against common security threats

## Getting Started

1. Install Django: `pip install django`
2. Create a new project: `django-admin startproject myproject`
3. Run the development server: `python manage.py runserver`

That's it! You now have a basic Django application running.''',
                'tags': 'Django, Python, Web Development',
                'is_published': True,
                'is_featured': True,
            },
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'slug': 'building-apis-with-drf',
                'excerpt': 'Learn how to create powerful REST APIs using Django REST Framework.',
                'body': '''# Building RESTful APIs with Django REST Framework

Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. It provides a flexible and powerful way to build REST APIs.

## Why Use DRF?

- **Serialization**: Easy conversion between Python objects and JSON
- **Authentication**: Multiple authentication schemes
- **Permissions**: Fine-grained permission system
- **Browsable API**: Interactive web interface for your API

## Basic Example

Here's a simple example of creating an API endpoint:

```python
from rest_framework import serializers, viewsets
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
```

This creates a full CRUD API for your Project model!''',
                'tags': 'Django REST Framework, API, Python',
                'is_published': True,
                'is_featured': False,
            },
        ]

        for blog_data in blog_posts_data:
            blog_post, created = BlogPost.objects.get_or_create(
                slug=blog_data['slug'],
                defaults=blog_data
            )
            if created:
                self.stdout.write(f'✅ Created blog post: {blog_post.title}')

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    PersonalInfo, Skill, CareerTimeline, Education, 
    Certification, Award, FooterLink, Project, Tag, SEOSettings
)
from datetime import date

class Command(BaseCommand):
    help = 'Set up comprehensive portfolio data for production deployment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up production portfolio data...'))
        
        # 1. Create or update PersonalInfo
        personal_info, created = PersonalInfo.objects.get_or_create(
            is_active=True,
            defaults={
                'portfolio_name': 'Peter Emmanuel\'s Portfolio',
                'full_name': 'Peter Emmanuel',
                'email': 'udohpeterbrown@gmail.com',
                'phone': '+2347033558942',
                'bio': 'Passionate full-stack developer with 3+ years of experience creating innovative web solutions using Django, React, and modern technologies.',
                'location': 'Nigeria',
                'about_intro': 'Welcome to my digital portfolio! I\'m a dedicated full-stack developer with a passion for creating robust, scalable web applications that solve real-world problems.',
                'years_experience': 3,
                'current_role': 'Full Stack Developer',
                'professional_summary': 'Experienced full-stack developer specializing in Python/Django backend development and modern frontend technologies. I have successfully delivered multiple client projects, focusing on responsive design, user experience optimization, and performance improvements.',
                'technical_skills': 'Python, Django, JavaScript, React, HTML5, CSS3, Bootstrap, PostgreSQL, MySQL, Git, Docker, Linux, AWS',
                'soft_skills': 'Problem Solving, Team Collaboration, Communication, Project Management, Attention to Detail',
                'interests': 'Web Development, Open Source, Technology Innovation, Continuous Learning',
                'github_url': 'https://github.com/emmanuelbrown',
                'linkedin_url': 'https://linkedin.com/in/emmanuelbrown',
                'twitter_url': 'https://twitter.com/emmanuelbrown',
                'meta_description': 'Peter Emmanuel - Full Stack Developer specializing in Django and React. View my portfolio showcasing web development projects and professional experience.',
                'meta_keywords': 'Peter Emmanuel, Full Stack Developer, Django Developer, React Developer, Web Development, Nigeria',
            }
        )
        
        if not created:
            # Update existing data with complete information
            personal_info.bio = 'Passionate full-stack developer with 3+ years of experience creating innovative web solutions using Django, React, and modern technologies.'
            personal_info.about_intro = 'Welcome to my digital portfolio! I\'m a dedicated full-stack developer with a passion for creating robust, scalable web applications that solve real-world problems.'
            personal_info.professional_summary = 'Experienced full-stack developer specializing in Python/Django backend development and modern frontend technologies. I have successfully delivered multiple client projects, focusing on responsive design, user experience optimization, and performance improvements.'
            personal_info.technical_skills = 'Python, Django, JavaScript, React, HTML5, CSS3, Bootstrap, PostgreSQL, MySQL, Git, Docker, Linux, AWS'
            personal_info.soft_skills = 'Problem Solving, Team Collaboration, Communication, Project Management, Attention to Detail'
            personal_info.interests = 'Web Development, Open Source, Technology Innovation, Continuous Learning'
            personal_info.save()
            self.stdout.write(self.style.SUCCESS('* Updated PersonalInfo with complete data'))
        else:
            self.stdout.write(self.style.SUCCESS('* Created comprehensive PersonalInfo'))

        # 2. Create Skills by category with detailed descriptions
        skills_data = {
            'frontend': [
                ('HTML5', 5, 'Expert in semantic HTML5, accessibility, and modern web standards'),
                ('CSS3', 5, 'Advanced CSS3, Flexbox, Grid, animations, and responsive design'),
                ('JavaScript', 4, 'ES6+, DOM manipulation, async programming, and modern JavaScript features'),
                ('React', 4, 'Component-based development, hooks, state management, and React ecosystem'),
                ('Bootstrap', 5, 'Expert in Bootstrap framework for rapid responsive UI development'),
                ('Tailwind CSS', 3, 'Utility-first CSS framework for modern web interfaces'),
            ],
            'backend': [
                ('Python', 5, 'Expert Python developer with strong OOP and functional programming skills'),
                ('Django', 5, 'Advanced Django development including REST APIs, authentication, and deployment'),
                ('REST APIs', 4, 'Design and implementation of RESTful web services and API endpoints'),
                ('Ajax', 4, 'Asynchronous web development and dynamic content loading'),
            ],
            'database': [
                ('MySQL', 4, 'Database design, optimization, and complex query development'),
                ('PostgreSQL', 4, 'Production-grade PostgreSQL database management and optimization'),
                ('SQLite', 5, 'Lightweight database for development and small applications'),
                ('MongoDB', 2, 'NoSQL database basics and document-based data modeling'),
            ],
            'tools': [
                ('Git', 5, 'Version control, branching strategies, and collaborative development'),
                ('Docker', 3, 'Containerization and deployment automation'),
                ('VS Code', 5, 'Advanced IDE usage with extensions and productivity workflows'),
                ('Linux', 4, 'Command line proficiency and server administration'),
            ],
            'devops': [
                ('CI/CD', 3, 'Continuous integration and deployment pipeline setup'),
                ('GitHub Actions', 3, 'Automated testing and deployment workflows'),
                ('AWS', 2, 'Cloud services basics and web application deployment'),
                ('Render', 4, 'Platform deployment and production environment management'),
            ]
        }
        
        for category, skills in skills_data.items():
            for skill_name, proficiency, description in skills:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    category=category,
                    defaults={
                        'proficiency': proficiency,
                        'description': description,
                        'is_featured': proficiency >= 4
                    }
                )
                if created:
                    self.stdout.write(f'* Created skill: {skill_name} ({category})')

        # 3. Create comprehensive Career Timeline
        career_entries = [
            {
                'job_title': 'Full Stack Developer',
                'company': 'Tech Solutions Inc',
                'company_url': '',
                'location': 'Remote',
                'job_type': 'fulltime',
                'start_date': date(2023, 1, 15),
                'is_current': True,
                'description': 'Lead full-stack developer responsible for designing and implementing scalable web applications using Django and React. Focus on responsive design, user experience optimization, and performance improvements for multiple client projects.',
                'technologies': 'Python, Django, React, JavaScript, PostgreSQL, Docker, Bootstrap, Git',
                'achievements': '• Increased application performance by 40% through database optimization and caching strategies\n• Successfully delivered 8+ client projects on time and within budget\n• Implemented responsive design principles reducing mobile bounce rate by 25%\n• Mentored junior developers and established coding standards',
                'order': 1
            },
            {
                'job_title': 'Junior Developer',
                'company': 'Uptech Computer Training Academy',
                'company_url': '',
                'location': 'Nigeria',
                'job_type': 'fulltime',
                'start_date': date(2022, 6, 1),
                'end_date': date(2023, 1, 10),
                'is_current': False,
                'description': 'Started professional career building web applications and learning modern development practices. Worked on various training projects while developing expertise in full-stack web development.',
                'technologies': 'HTML, CSS, JavaScript, Python, Django, MySQL, Bootstrap',
                'achievements': '• Successfully completed 5 comprehensive training projects\n• Earned full-stack web development certification\n• Developed strong foundation in Django framework and database design\n• Collaborated effectively in team development environments',
                'order': 2
            }
        ]
        
        for entry_data in career_entries:
            career, created = CareerTimeline.objects.get_or_create(
                job_title=entry_data['job_title'],
                company=entry_data['company'],
                defaults=entry_data
            )
            if created:
                self.stdout.write(f'* Created career entry: {entry_data["job_title"]} at {entry_data["company"]}')

        # 4. Create Education entries
        education_entries = [
            {
                'school_name': 'Divine Sound College',
                'degree': 'Senior Secondary Certificate',
                'field_of_study': 'Science',
                'start_date': date(2018, 9, 1),
                'end_date': date(2023, 6, 15),
                'grade': 'Good',
                'description': 'Completed secondary education with focus on science subjects, building strong analytical and problem-solving skills that form the foundation for technical career development.',
                'location': 'Nigeria',
                'order': 1
            },
            {
                'school_name': 'Uptech Computer Training Academy',
                'degree': 'Certificate in Web Development',
                'field_of_study': 'Computer Science',
                'start_date': date(2022, 1, 1),
                'end_date': date(2022, 12, 31),
                'grade': 'Excellent',
                'description': 'Comprehensive training in modern web development technologies including Python, Django, JavaScript, and frontend frameworks. Gained hands-on experience through multiple real-world projects.',
                'location': 'Nigeria',
                'order': 2
            }
        ]
        
        for edu_data in education_entries:
            education, created = Education.objects.get_or_create(
                school_name=edu_data['school_name'],
                degree=edu_data['degree'],
                defaults=edu_data
            )
            if created:
                self.stdout.write(f'* Created education: {edu_data["degree"]} from {edu_data["school_name"]}')

        # 5. Create Certifications with detailed descriptions
        cert_data = [
            {
                'name': 'Django Web Development',
                'issuing_organization': 'Uptech Academy',
                'issue_date': date(2022, 12, 15),
                'description': 'Comprehensive certification covering Django framework development, including models, views, templates, authentication, REST APIs, and deployment strategies.',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'JavaScript Fundamentals',
                'issuing_organization': 'Online Learning Platform',
                'issue_date': date(2022, 8, 20),
                'description': 'Advanced JavaScript certification covering ES6+ features, asynchronous programming, DOM manipulation, and modern development practices.',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Full Stack Web Development',
                'issuing_organization': 'Uptech Academy',
                'issue_date': date(2023, 1, 10),
                'description': 'Complete full-stack development certification demonstrating proficiency in both frontend and backend technologies, database management, and deployment.',
                'is_featured': True,
                'order': 3
            }
        ]
        
        for cert in cert_data:
            certification, created = Certification.objects.get_or_create(
                name=cert['name'],
                issuing_organization=cert['issuing_organization'],
                defaults=cert
            )
            if created:
                self.stdout.write(f'* Created certification: {cert["name"]}')

        # 6. Create Awards
        awards_data = [
            {
                'title': 'Best Student Project',
                'issuing_organization': 'Uptech Academy',
                'date_received': date(2022, 12, 20),
                'description': 'Recognized for developing the most innovative and well-executed final project in the web development program.',
                'category': 'Academic',
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Excellence in Web Development',
                'issuing_organization': 'Uptech Academy',
                'date_received': date(2023, 1, 15),
                'description': 'Awarded for outstanding performance and dedication throughout the comprehensive web development training program.',
                'category': 'Academic',
                'is_featured': True,
                'order': 2
            }
        ]
        
        for award in awards_data:
            award_obj, created = Award.objects.get_or_create(
                title=award['title'],
                issuing_organization=award['issuing_organization'],
                defaults=award
            )
            if created:
                self.stdout.write(f'* Created award: {award["title"]}')

        # 7. Create Footer Links
        footer_links_data = [
            ('Home', '/', 'quick', 'bi bi-house', False, True, 1),
            ('About', '/about/', 'quick', 'bi bi-person', False, True, 2),
            ('Projects', '/projects/', 'quick', 'bi bi-folder', False, True, 3),
            ('Blog', '/blog/', 'quick', 'bi bi-journal', False, True, 4),
            ('Contact', '/contact/', 'quick', 'bi bi-envelope', False, True, 5),
            ('LinkedIn', 'https://linkedin.com/in/emmanuelbrown', 'social', 'bi bi-linkedin', True, True, 1),
            ('GitHub', 'https://github.com/emmanuelbrown', 'social', 'bi bi-github', True, True, 2),
            ('Twitter', 'https://twitter.com/emmanuelbrown', 'social', 'bi bi-twitter', True, True, 3),
        ]
        
        for title, url, category, icon, is_external, is_active, order in footer_links_data:
            link, created = FooterLink.objects.get_or_create(
                title=title,
                category=category,
                defaults={
                    'url': url,
                    'icon_class': icon,
                    'is_external': is_external,
                    'is_active': is_active,
                    'order': order
                }
            )
            if created:
                self.stdout.write(f'* Created footer link: {title} ({category})')

        # 8. Create sample projects with tags
        tags_data = ['Python', 'Django', 'JavaScript', 'React', 'HTML/CSS', 'Bootstrap', 'PostgreSQL', 'REST API']
        tag_objects = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
            if created:
                self.stdout.write(f'* Created tag: {tag_name}')

        projects_data = [
            {
                'title': 'Portfolio Website',
                'slug': 'portfolio-website',
                'description': 'A comprehensive portfolio website built with Django and Bootstrap, featuring dynamic content management, responsive design, and SEO optimization.',
                'tech_stack': 'Django, Python, Bootstrap, PostgreSQL, JavaScript',
                'live_url': 'https://your-portfolio.onrender.com',
                'repo_url': 'https://github.com/emmanuelbrown/portfolio',
                'is_featured': True,
                'tags': ['Django', 'Python', 'Bootstrap', 'PostgreSQL']
            },
            {
                'title': 'E-commerce Dashboard',
                'slug': 'ecommerce-dashboard',
                'description': 'A modern e-commerce management dashboard with real-time analytics, inventory management, and customer relationship features.',
                'tech_stack': 'Django, React, PostgreSQL, REST API',
                'live_url': '',
                'repo_url': 'https://github.com/emmanuelbrown/ecommerce-dashboard',
                'is_featured': True,
                'tags': ['Django', 'React', 'REST API', 'PostgreSQL']
            },
            {
                'title': 'Task Management System',
                'slug': 'task-management-system',
                'description': 'A collaborative task management application with team features, deadline tracking, and progress visualization.',
                'tech_stack': 'Django, JavaScript, Bootstrap, MySQL',
                'live_url': '',
                'repo_url': 'https://github.com/emmanuelbrown/task-manager',
                'is_featured': False,
                'tags': ['Django', 'JavaScript', 'Bootstrap']
            }
        ]

        for project_data in projects_data:
            project_tags = project_data.pop('tags', [])
            project, created = Project.objects.get_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )
            if created:
                # Add tags to project
                for tag_name in project_tags:
                    tag = Tag.objects.get(name=tag_name)
                    project.tags.add(tag)
                self.stdout.write(f'* Created project: {project_data["title"]}')

        # 9. Create SEO Settings
        seo_data = [
            {
                'page': 'home',
                'title': 'Peter Emmanuel - Full Stack Developer',
                'description': 'Professional portfolio of Peter Emmanuel, a full stack developer specializing in Django and React development in Nigeria.',
                'keywords': 'Peter Emmanuel, Full Stack Developer, Django, React, Web Development, Nigeria',
            },
            {
                'page': 'about',
                'title': 'About Peter Emmanuel - Full Stack Developer',
                'description': 'Learn about Peter Emmanuel\'s professional journey, skills, education, and experience in full stack web development.',
                'keywords': 'About Peter Emmanuel, Developer Experience, Skills, Education, Career',
            },
            {
                'page': 'projects',
                'title': 'Projects by Peter Emmanuel - Web Development Portfolio',
                'description': 'Explore web development projects by Peter Emmanuel, showcasing Django, React, and full stack development skills.',
                'keywords': 'Web Development Projects, Django Projects, React Projects, Portfolio',
            },
            {
                'page': 'contact',
                'title': 'Contact Peter Emmanuel - Full Stack Developer',
                'description': 'Get in touch with Peter Emmanuel for web development projects, collaboration, or professional opportunities.',
                'keywords': 'Contact Peter Emmanuel, Web Developer Contact, Hire Developer, Collaboration',
            },
        ]

        for seo in seo_data:
            seo_obj, created = SEOSettings.objects.get_or_create(
                page=seo['page'],
                defaults=seo
            )
            if created:
                self.stdout.write(f'* Created SEO settings for: {seo["page"]} page')

        # 10. Create admin user if needed
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('* Created admin user (username: admin, password: admin123)'))

        self.stdout.write(self.style.SUCCESS('\nProduction portfolio data setup complete!'))
        self.stdout.write(self.style.SUCCESS('* All personal information, skills, career timeline, education, and certifications have been set up'))
        self.stdout.write(self.style.SUCCESS('* Projects, footer links, and SEO settings are configured'))
        self.stdout.write(self.style.SUCCESS('* Your portfolio is now ready for production with complete data'))
        self.stdout.write(self.style.SUCCESS('\nNext steps:'))
        self.stdout.write(self.style.SUCCESS('1. Deploy to Render with PostgreSQL database'))
        self.stdout.write(self.style.SUCCESS('2. Verify all content displays correctly'))
        self.stdout.write(self.style.SUCCESS('3. Access admin dashboard to manage content'))

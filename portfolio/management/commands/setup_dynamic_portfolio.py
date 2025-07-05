from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    PersonalInfo, Skill, CareerTimeline, Education, 
    Certification, Award, FooterLink
)
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Create sample dynamic portfolio content for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up dynamic portfolio content...'))
        
        # Create or update PersonalInfo
        personal_info, created = PersonalInfo.objects.get_or_create(
            is_active=True,
            defaults={
                'portfolio_name': 'Peter Emmanuel\'s Portfolio',
                'full_name': 'Peter Emmanuel',
                'email': 'emmanuelmikebrown242@yahoo.com',
                'phone': '+2349123721167',
                'bio': 'Passionate full-stack developer creating innovative solutions with modern technologies.',
                'location': 'Nigeria',
                'about_intro': 'Welcome to my digital portfolio! I\'m a dedicated developer with a passion for creating robust web applications.',
                'years_experience': 3,
                'current_role': 'Full Stack Developer',
                'professional_summary': 'Experienced in building scalable web applications using Django, React, and modern development practices.',
                'github_url': 'https://github.com/emmanuelbrown',
                'linkedin_url': 'https://linkedin.com/in/emmanuelbrown',
                'twitter_url': 'https://twitter.com/emmanuelbrown',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created PersonalInfo'))
        else:
            # Update years of experience for testing
            personal_info.years_experience = 3
            personal_info.save()
            self.stdout.write(self.style.SUCCESS('✓ Updated PersonalInfo'))

        # Create Skills by category
        skills_data = {
            'frontend': [
                ('HTML5', 5), ('CSS3', 5), ('JavaScript', 4), ('React', 4), 
                ('Bootstrap', 5), ('Tailwind CSS', 3)
            ],
            'backend': [
                ('Python', 5), ('Django', 5), ('REST APIs', 4), ('Ajax', 4)
            ],
            'database': [
                ('MySQL', 4), ('PostgreSQL', 3), ('SQLite', 5), ('MongoDB', 2)
            ],
            'tools': [
                ('Git', 5), ('Docker', 3), ('VS Code', 5), ('Linux', 4)
            ],
            'devops': [
                ('CI/CD', 3), ('GitHub Actions', 3), ('AWS', 2)
            ]
        }
        
        for category, skills in skills_data.items():
            for skill_name, proficiency in skills:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    category=category,
                    defaults={
                        'proficiency': proficiency,
                        'is_featured': proficiency >= 4
                    }
                )
                if created:
                    self.stdout.write(f'✓ Created skill: {skill_name} ({category})')

        # Create Career Timeline
        career_entries = [
            {
                'job_title': 'Full Stack Developer',
                'company': 'Tech Solutions Inc',
                'location': 'Remote',
                'job_type': 'fulltime',
                'start_date': date(2023, 1, 15),
                'is_current': True,
                'description': 'Developing and maintaining multiple client projects using Django and React. Focus on responsive design and user experience optimization.',
                'technologies': 'Python, Django, React, JavaScript, PostgreSQL, Docker',
                'achievements': 'Increased application performance by 40% through optimization techniques and database improvements.',
                'order': 1
            },
            {
                'job_title': 'Junior Developer',
                'company': 'Uptech Computer Training Academy',
                'location': 'Nigeria',
                'job_type': 'fulltime',
                'start_date': date(2022, 6, 1),
                'end_date': date(2023, 1, 10),
                'is_current': False,
                'description': 'Started my career building web applications and learning modern development practices. Worked on various training projects.',
                'technologies': 'HTML, CSS, JavaScript, Python, Django',
                'achievements': 'Successfully completed 5 training projects and earned certification in web development.',
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
                self.stdout.write(f'✓ Created career entry: {entry_data["job_title"]} at {entry_data["company"]}')

        # Create Education entries
        education_entries = [
            {
                'school_name': 'Divine Sound College',
                'degree': 'Senior Secondary Certificate',
                'field_of_study': 'Science',
                'start_date': date(2018, 9, 1),
                'end_date': date(2023, 6, 15),
                'grade': 'Good',
                'description': 'Completed secondary education with focus on science subjects.',
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
                'description': 'Comprehensive training in modern web development technologies including Python, Django, and frontend frameworks.',
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
                self.stdout.write(f'✓ Created education: {edu_data["degree"]} from {edu_data["school_name"]}')

        # Create sample Certifications
        cert_data = [
            {
                'name': 'Django Web Development',
                'issuing_organization': 'Uptech Academy',
                'issue_date': date(2022, 12, 15),
                'description': 'Comprehensive certification in Django framework development.',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'JavaScript Fundamentals',
                'issuing_organization': 'Online Learning Platform',
                'issue_date': date(2022, 8, 20),
                'description': 'Certification in modern JavaScript development practices.',
                'is_featured': True,
                'order': 2
            }
        ]
        
        for cert in cert_data:
            certification, created = Certification.objects.get_or_create(
                name=cert['name'],
                issuing_organization=cert['issuing_organization'],
                defaults=cert
            )
            if created:
                self.stdout.write(f'✓ Created certification: {cert["name"]}')

        # Create Footer Links
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
                self.stdout.write(f'✓ Created footer link: {title} ({category})')

        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created admin user (username: admin, password: admin123)'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Dynamic portfolio setup complete!'))
        self.stdout.write(self.style.SUCCESS('You can now:'))
        self.stdout.write(self.style.SUCCESS('1. Run the server: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('2. Visit the About page to see dynamic content'))
        self.stdout.write(self.style.SUCCESS('3. Login to dashboard with admin/admin123'))
        self.stdout.write(self.style.SUCCESS('4. Manage all content from the dashboard'))

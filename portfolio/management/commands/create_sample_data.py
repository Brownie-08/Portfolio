from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from portfolio.models import Tag, Project, Testimonial, BlogPost, ContactMessage


class Command(BaseCommand):
    help = 'Create sample data for testing admin interface'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create tags
        tags = ['Python', 'Django', 'JavaScript', 'React', 'HTML/CSS', 'Bootstrap']
        tag_objects = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')
        
        # Create projects
        for i in range(3):
            test_image = self.create_test_image(f"project_{i+1}.jpg", color="blue")
            project, created = Project.objects.get_or_create(
                slug=f'sample-project-{i+1}',
                defaults={
                    'title': f'Sample Project {i+1}',
                    'description': f'This is a sample project #{i+1} created for testing the admin interface.',
                    'tech_stack': ', '.join([tag.name for tag in tag_objects[:3]]),
                    'image': test_image,
                    'live_url': f'https://example.com/project{i+1}',
                    'repo_url': f'https://github.com/user/project{i+1}',
                    'is_featured': i == 0  # Make first project featured
                }
            )
            if created:
                project.tags.add(*tag_objects[:3])
                self.stdout.write(f'Created project: {project.title}')
        
        # Create testimonials
        testimonials_data = [
            ('John Doe', 'CEO at TechCorp', 'Excellent work on our web application!'),
            ('Jane Smith', 'Project Manager at StartupXYZ', 'Very professional and delivered on time.'),
            ('Mike Johnson', 'CTO at InnovateCo', 'Outstanding technical skills and communication.'),
        ]
        
        for i, (name, role, comment) in enumerate(testimonials_data):
            avatar = self.create_test_image(f"avatar_{i+1}.jpg", size=(150, 150), color="green")
            testimonial, created = Testimonial.objects.get_or_create(
                name=name,
                defaults={
                    'role': role,
                    'comment': comment,
                    'avatar': avatar,
                    'is_featured': i == 0  # Make first testimonial featured
                }
            )
            if created:
                self.stdout.write(f'Created testimonial: {testimonial.name}')
        
        # Create blog posts
        for i in range(2):
            blog_image = self.create_test_image(f"blog_{i+1}.jpg", size=(800, 400), color="purple")
            blog_post, created = BlogPost.objects.get_or_create(
                slug=f'sample-blog-post-{i+1}',
                defaults={
                    'title': f'Sample Blog Post {i+1}',
                    'excerpt': f'This is a sample blog post excerpt #{i+1} for testing purposes.',
                    'body': f'This is the full content of sample blog post #{i+1}. It contains detailed information about the topic.',
                    'image': blog_image,
                    'is_published': True
                }
            )
            if created:
                self.stdout.write(f'Created blog post: {blog_post.title}')
        
        # Create contact messages
        contact_messages_data = [
            ('Alice Brown', 'alice@example.com', 'Project Inquiry', 'I would like to discuss a potential project.'),
            ('Bob Wilson', 'bob@example.com', 'Collaboration', 'Interested in collaborating on a startup idea.'),
            ('Carol Davis', 'carol@example.com', 'Job Opportunity', 'We have an exciting job opportunity for you.'),
        ]
        
        for i, (name, email, subject, message) in enumerate(contact_messages_data):
            contact_message, created = ContactMessage.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'subject': subject,
                    'message': message,
                    'is_read': i == 0  # Mark first message as read
                }
            )
            if created:
                self.stdout.write(f'Created contact message from: {contact_message.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
    
    def create_test_image(self, filename, size=(800, 600), color="blue"):
        """Create a simple test image"""
        img = Image.new('RGB', size, color=color)
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return SimpleUploadedFile(
            filename,
            img_io.getvalue(),
            content_type='image/jpeg'
        )

from django.core.management.base import BaseCommand
from portfolio.models import BlogPost


class Command(BaseCommand):
    help = 'Check and verify blog posts configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking blog posts configuration...'))
        
        # Get all blog posts
        all_posts = BlogPost.objects.all()
        published_posts = BlogPost.objects.filter(is_published=True)
        featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)
        
        self.stdout.write(f'📊 Blog Posts Summary:')
        self.stdout.write(f'  Total posts: {all_posts.count()}')
        self.stdout.write(f'  Published posts: {published_posts.count()}')
        self.stdout.write(f'  Featured posts: {featured_posts.count()}')
        
        self.stdout.write(f'\n📝 All Blog Posts:')
        for i, post in enumerate(all_posts, 1):
            status = "✅ Published" if post.is_published else "❌ Draft"
            featured = " ⭐ Featured" if post.is_featured else ""
            self.stdout.write(f'  {i}. {post.title}')
            self.stdout.write(f'     Status: {status}{featured}')
            self.stdout.write(f'     Slug: {post.slug}')
            self.stdout.write(f'     Created: {post.created}')
            self.stdout.write(f'     Tags: {post.tags or "No tags"}')
            if post.excerpt:
                self.stdout.write(f'     Excerpt: {post.excerpt[:100]}...')
            self.stdout.write('')
        
        # Check if any posts need to be made featured
        if featured_posts.count() == 0:
            self.stdout.write(self.style.WARNING('⚠️  No featured posts found. Setting first 2 posts as featured...'))
            first_posts = published_posts[:2]
            for post in first_posts:
                post.is_featured = True
                post.save()
                self.stdout.write(f'✅ Set {post.title} as featured')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Blog posts check complete!'))

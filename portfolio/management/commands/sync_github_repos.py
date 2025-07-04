import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from portfolio.models import Project, Tag
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Sync GitHub repositories to projects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='GitHub username to fetch repositories from',
            default='your-github-username'
        )
        parser.add_argument(
            '--token',
            type=str,
            help='GitHub personal access token (optional but recommended)',
        )
        parser.add_argument(
            '--max-repos',
            type=int,
            default=10,
            help='Maximum number of repositories to sync',
        )

    def handle(self, *args, **options):
        username = options['username']
        token = options.get('token') or os.getenv('GITHUB_TOKEN')
        max_repos = options['max_repos']
        
        self.stdout.write(f'Syncing GitHub repositories for user: {username}')
        
        # GitHub API headers
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
            self.stdout.write('Using GitHub token for authentication')
        
        try:
            # Fetch repositories from GitHub API
            url = f'https://api.github.com/users/{username}/repos'
            params = {
                'type': 'owner',
                'sort': 'updated',
                'per_page': max_repos
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            repos = response.json()
            
            created_count = 0
            updated_count = 0
            
            for repo_data in repos:
                # Skip private repos unless they're explicitly featured
                if repo_data['private']:
                    continue
                
                # Extract relevant data
                repo_name = f"{username}/{repo_data['name']}"
                title = repo_data['name'].replace('-', ' ').replace('_', ' ').title()
                description = repo_data.get('description') or f'A {repo_data.get("language", "software")} project'
                
                # Create or update project
                project, created = Project.objects.get_or_create(
                    github_repo=repo_name,
                    defaults={
                        'title': title,
                        'slug': slugify(title),
                        'description': description,
                        'tech_stack': self._get_tech_stack(repo_data),
                        'repo_url': repo_data['html_url'],
                        'live_url': self._get_live_url(repo_data),
                        'is_github_synced': True,
                        'github_stars': repo_data['stargazers_count'],
                        'github_forks': repo_data['forks_count'],
                        'github_language': repo_data.get('language') or '',
                        'github_updated_at': timezone.now(),
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created project: {project.title}')
                    )
                    
                    # Add tags based on language and topics
                    self._add_tags(project, repo_data)
                    
                else:
                    # Update existing project with latest GitHub data
                    project.github_stars = repo_data['stargazers_count']
                    project.github_forks = repo_data['forks_count']
                    project.github_language = repo_data.get('language') or ''
                    project.github_updated_at = timezone.now()
                    
                    # Update description if it wasn't manually set
                    if project.is_github_synced and repo_data.get('description'):
                        project.description = repo_data['description']
                    
                    project.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated project: {project.title}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully synced {len(repos)} repositories: '
                    f'{created_count} created, {updated_count} updated'
                )
            )
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching GitHub repositories: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )

    def _get_tech_stack(self, repo_data):
        """Extract tech stack from repository data"""
        tech_stack = []
        
        # Add primary language
        if repo_data.get('language'):
            tech_stack.append(repo_data['language'])
        
        # Add topics if available
        if repo_data.get('topics'):
            tech_stack.extend(repo_data['topics'][:5])  # Limit to 5 topics
        
        return ', '.join(tech_stack) if tech_stack else 'Open Source'

    def _get_live_url(self, repo_data):
        """Extract live URL from repository data"""
        # Check homepage field
        if repo_data.get('homepage'):
            return repo_data['homepage']
        
        # Check for GitHub Pages
        if repo_data.get('has_pages'):
            return f"https://{repo_data['owner']['login']}.github.io/{repo_data['name']}"
        
        return ''

    def _add_tags(self, project, repo_data):
        """Add tags to project based on repository data"""
        tag_names = set()
        
        # Add language as tag
        if repo_data.get('language'):
            tag_names.add(repo_data['language'])
        
        # Add topics as tags
        if repo_data.get('topics'):
            tag_names.update(repo_data['topics'][:3])  # Limit to 3 topics
        
        # Add 'GitHub' tag to indicate it's synced
        tag_names.add('GitHub')
        
        # Create or get tags and add to project
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)

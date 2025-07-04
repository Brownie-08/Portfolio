from django.core.management.base import BaseCommand
from portfolio.models import BlogPost
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create realistic blog content for portfolio'

    def handle(self, *args, **options):
        self.stdout.write('Creating realistic blog content...')
        
        # Delete existing blog posts
        BlogPost.objects.all().delete()
        
        blog_posts = [
            {
                'title': 'Building Scalable Web Applications with Django',
                'slug': 'building-scalable-web-applications-django',
                'excerpt': 'Explore best practices for developing robust and scalable web applications using Django framework, covering performance optimization, security, and deployment strategies.',
                'body': '''
Building scalable web applications is a critical skill for modern developers. Django, with its "batteries included" philosophy, provides an excellent foundation for creating robust applications that can handle growing user bases and complex requirements.

## Why Django for Scalability?

Django offers several features that make it ideal for scalable applications:

### 1. ORM Optimization
Django's ORM provides powerful tools for database optimization:
- Select related and prefetch related for reducing queries
- Database indexing support
- Query optimization tools

### 2. Caching Framework
Built-in caching support with multiple backends:
- Redis integration
- Memcached support
- Database caching
- File-based caching

### 3. Middleware Architecture
Flexible middleware system for:
- Authentication and authorization
- Request/response processing
- Security enhancements
- Performance monitoring

## Best Practices for Scale

### Database Optimization
```python
# Use select_related for foreign keys
posts = BlogPost.objects.select_related('author').all()

# Use prefetch_related for many-to-many relationships
posts = BlogPost.objects.prefetch_related('tags').all()
```

### Caching Strategies
Implement strategic caching at multiple levels:
- Template fragment caching
- View-level caching
- Database query caching
- Static file caching

### Performance Monitoring
Monitor your application performance with:
- Django Debug Toolbar for development
- APM tools for production
- Database query analysis
- Memory usage tracking

## Deployment Considerations

For production deployments, consider:
- Load balancing with nginx
- Database replication
- CDN integration
- Container orchestration with Docker

Scaling Django applications requires careful planning and implementation of best practices, but the framework provides all the tools necessary for building applications that can grow with your business needs.
                ''',
                'tags': 'Django,Web Development,Scalability,Performance,Backend',
                'is_featured': True,
                'is_published': True,
                'created': datetime.now() - timedelta(days=5)
            },
            {
                'title': 'Modern Frontend Development with React and TypeScript',
                'slug': 'modern-frontend-development-react-typescript',
                'excerpt': 'Dive into modern frontend development practices using React with TypeScript, exploring component architecture, state management, and development workflows.',
                'body': '''
The frontend development landscape has evolved dramatically over the past few years. React, combined with TypeScript, has become a powerful combination for building maintainable and scalable user interfaces.

## Why React + TypeScript?

The combination of React and TypeScript offers several advantages:

### Type Safety
TypeScript provides compile-time type checking, catching errors before they reach production:
```typescript
interface UserProps {
  name: string;
  email: string;
  isActive: boolean;
}

const UserComponent: React.FC<UserProps> = ({ name, email, isActive }) => {
  return (
    <div className={`user ${isActive ? 'active' : 'inactive'}`}>
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};
```

### Better Developer Experience
- Autocomplete and IntelliSense
- Refactoring support
- Enhanced debugging capabilities

## Component Architecture

### Functional Components with Hooks
Modern React development focuses on functional components:
```typescript
import { useState, useEffect } from 'react';

const DataComponent: React.FC = () => {
  const [data, setData] = useState<ApiData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return loading ? <Spinner /> : <DataList data={data} />;
};
```

### Custom Hooks
Create reusable logic with custom hooks:
```typescript
const useApi = <T>(url: string) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(response => response.json())
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
};
```

## State Management

For complex applications, consider:
- React Context for theme/auth
- Redux Toolkit for complex state
- Zustand for lightweight state management
- SWR or React Query for server state

## Testing Strategy

Implement comprehensive testing:
- Unit tests with Jest
- Component testing with React Testing Library
- Integration tests
- End-to-end tests with Cypress

The React and TypeScript ecosystem continues to evolve, providing developers with powerful tools for building modern, maintainable web applications.
                ''',
                'tags': 'React,TypeScript,Frontend,JavaScript,Modern Development',
                'is_featured': True,
                'is_published': True,
                'created': datetime.now() - timedelta(days=12)
            },
            {
                'title': 'Database Design Patterns for Modern Applications',
                'slug': 'database-design-patterns-modern-applications',
                'excerpt': 'Explore essential database design patterns and practices for building efficient and maintainable data layers in modern applications.',
                'body': '''
Database design is the foundation of any successful application. Poor database design can lead to performance issues, data inconsistencies, and maintenance nightmares. Let's explore proven patterns and practices for modern database design.

## Fundamental Design Principles

### Normalization vs. Denormalization
Understanding when to normalize and when to denormalize:

**Normalization Benefits:**
- Reduced data redundancy
- Improved data integrity
- Easier maintenance

**Denormalization Benefits:**
- Improved query performance
- Simplified queries
- Better read performance

### ACID Properties
Ensure your database transactions maintain:
- **Atomicity**: All operations succeed or fail together
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

## Common Design Patterns

### 1. Repository Pattern
Abstract database operations behind a clean interface:
```python
class UserRepository:
    def get_by_id(self, user_id: int) -> User:
        return User.objects.get(id=user_id)
    
    def get_active_users(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)
    
    def create_user(self, data: dict) -> User:
        return User.objects.create(**data)
```

### 2. Unit of Work Pattern
Manage transactions and maintain object state:
```python
class UnitOfWork:
    def __init__(self):
        self._new_objects = []
        self._dirty_objects = []
        self._removed_objects = []
    
    def register_new(self, obj):
        self._new_objects.append(obj)
    
    def commit(self):
        with transaction.atomic():
            for obj in self._new_objects:
                obj.save()
            # Handle dirty and removed objects
```

### 3. Data Mapper Pattern
Separate domain objects from database concerns:
```python
class UserMapper:
    @staticmethod
    def to_domain(row: dict) -> User:
        return User(
            id=row['id'],
            name=row['name'],
            email=row['email']
        )
    
    @staticmethod
    def to_persistence(user: User) -> dict:
        return {
            'name': user.name,
            'email': user.email
        }
```

## Performance Optimization

### Indexing Strategies
- Primary indexes on ID fields
- Secondary indexes on frequently queried fields
- Composite indexes for multi-column queries
- Partial indexes for conditional queries

### Query Optimization
- Use EXPLAIN to analyze query plans
- Avoid N+1 query problems
- Implement query result caching
- Consider read replicas for read-heavy workloads

### Connection Pooling
Manage database connections efficiently:
- Configure appropriate pool sizes
- Monitor connection usage
- Implement connection timeouts
- Use connection pooling libraries

## Modern Database Considerations

### Microservices and Data
- Database per service pattern
- Event sourcing for audit trails
- CQRS for read/write separation
- Eventual consistency patterns

### Cloud-Native Patterns
- Auto-scaling databases
- Multi-region replication
- Backup and disaster recovery
- Monitoring and alerting

Proper database design requires balancing performance, consistency, and maintainability. Choose patterns that align with your application's specific requirements and scale characteristics.
                ''',
                'tags': 'Database,Design Patterns,Performance,SQL,Architecture',
                'is_featured': False,
                'is_published': True,
                'created': datetime.now() - timedelta(days=18)
            },
            {
                'title': 'DevOps Best Practices: CI/CD Pipelines with GitHub Actions',
                'slug': 'devops-best-practices-cicd-github-actions',
                'excerpt': 'Learn how to implement robust CI/CD pipelines using GitHub Actions, including testing, deployment, and monitoring strategies.',
                'body': '''
Continuous Integration and Continuous Deployment (CI/CD) have become essential practices in modern software development. GitHub Actions provides a powerful platform for implementing these practices directly within your Git workflow.

## Understanding CI/CD

### Continuous Integration (CI)
Automatically integrate code changes:
- Run automated tests on every commit
- Ensure code quality and standards
- Detect integration issues early
- Maintain a always-deployable main branch

### Continuous Deployment (CD)
Automate the deployment process:
- Deploy to staging environments automatically
- Run acceptance tests
- Deploy to production with approval gates
- Monitor deployment health

## GitHub Actions Fundamentals

### Basic Workflow Structure
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=./ --cov-report=xml
```

### Advanced Workflow Features
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```

## Deployment Strategies

### Environment Management
```yaml
deploy-staging:
  needs: test
  runs-on: ubuntu-latest
  environment: staging
  steps:
    - name: Deploy to staging
      run: |
        echo "Deploying to staging..."

deploy-production:
  needs: deploy-staging
  runs-on: ubuntu-latest
  environment: production
  if: github.ref == 'refs/heads/main'
  steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
```

### Secret Management
Use GitHub Secrets for sensitive data:
```yaml
- name: Deploy to cloud
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    deploy-script.sh
```

## Quality Gates

### Code Quality Checks
```yaml
quality:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Run linting
      run: |
        flake8 .
        black --check .
        mypy .
    - name: Security scan
      run: |
        bandit -r .
        safety check
```

### Test Coverage
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

## Monitoring and Notifications

### Slack Integration
```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Performance Monitoring
```yaml
- name: Performance tests
  run: |
    locust --headless --users 10 --spawn-rate 2 -t 30s
```

## Best Practices

### 1. Fail Fast
Structure workflows to fail quickly on common issues:
- Run linting before tests
- Run unit tests before integration tests
- Use dependency caching

### 2. Parallel Execution
Run independent jobs in parallel:
- Separate test and build jobs
- Matrix builds for multiple environments
- Parallel deployment to different regions

### 3. Artifact Management
```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v3
  with:
    name: build-artifacts
    path: dist/
```

### 4. Security Considerations
- Use least-privilege principles
- Regularly rotate secrets
- Audit third-party actions
- Monitor for security vulnerabilities

Implementing robust CI/CD pipelines with GitHub Actions enables teams to deliver high-quality software faster and more reliably. Start with basic workflows and gradually add sophistication as your needs grow.
                ''',
                'tags': 'DevOps,CI/CD,GitHub Actions,Automation,Deployment',
                'is_featured': False,
                'is_published': True,
                'created': datetime.now() - timedelta(days=25)
            },
            {
                'title': 'API Design: Building RESTful Services That Scale',
                'slug': 'api-design-building-restful-services-scale',
                'excerpt': 'Master the art of designing robust RESTful APIs that can handle growth, maintain consistency, and provide excellent developer experience.',
                'body': '''
API design is both an art and a science. A well-designed API can be the difference between a successful product and one that struggles with adoption. Let's explore the principles and practices for building RESTful services that scale.

## REST Principles

### Resource-Oriented Design
Design your API around resources, not actions:
```
Good: GET /users/123
Bad:  GET /getUser?id=123

Good: POST /users
Bad:  POST /createUser

Good: PUT /users/123
Bad:  POST /updateUser?id=123
```

### HTTP Methods and Status Codes
Use HTTP methods correctly:
- **GET**: Retrieve resources (idempotent)
- **POST**: Create new resources
- **PUT**: Update/replace entire resource (idempotent)
- **PATCH**: Partial updates
- **DELETE**: Remove resources (idempotent)

Return appropriate status codes:
- **200**: Success
- **201**: Created
- **204**: No Content
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **422**: Unprocessable Entity
- **500**: Internal Server Error

## API Versioning Strategies

### URL Versioning
```
/v1/users
/v2/users
```

### Header Versioning
```
Accept: application/vnd.myapi.v1+json
```

### Parameter Versioning
```
/users?version=1
```

## Request and Response Design

### Consistent Naming Conventions
```json
{
  "user_id": 123,
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

### Pagination
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false
  }
}
```

### Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email address is required"
      }
    ]
  }
}
```

## Security Best Practices

### Authentication and Authorization
```python
# JWT Token Authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
```

### Input Validation
```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
```

### Rate Limiting
```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

## Performance Optimization

### Caching Strategies
```python
from django.core.cache import cache
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    def list(self, request):
        cache_key = f"users_list_{request.query_params.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        data = self.get_serializer(self.get_queryset(), many=True).data
        cache.set(cache_key, data, timeout=300)  # 5 minutes
        return Response(data)
```

### Database Optimization
```python
class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.select_related('profile').prefetch_related('roles')
```

### Filtering and Searching
```python
from django_filters import rest_framework as filters

class UserFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    
    class Meta:
        model = User
        fields = ['is_active', 'role']
```

## Documentation and Testing

### API Documentation
Use tools like Swagger/OpenAPI:
```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_description="Create a new user",
        responses={201: UserSerializer}
    )
    def create(self, request):
        pass
```

### Automated Testing
```python
from rest_framework.test import APITestCase
from rest_framework import status

class UserAPITests(APITestCase):
    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
```

## Monitoring and Analytics

### API Metrics
Track important metrics:
- Response times
- Error rates
- Request volumes
- Most used endpoints

### Logging
```python
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    def create(self, request):
        logger.info(f"Creating user: {request.data.get('username')}")
        # ... creation logic
        logger.info(f"User created successfully: {user.id}")
```

Building scalable RESTful APIs requires careful attention to design principles, security, performance, and maintainability. Start with solid foundations and iterate based on real-world usage patterns and feedback.
                ''',
                'tags': 'API Design,REST,Backend,Web Services,Architecture',
                'is_featured': False,
                'is_published': True,
                'created': datetime.now() - timedelta(days=32)
            },
            {
                'title': 'Python Performance Optimization: From Slow to Fast',
                'slug': 'python-performance-optimization-slow-to-fast',
                'excerpt': 'Discover practical techniques for optimizing Python applications, from profiling and algorithmic improvements to advanced optimization strategies.',
                'body': '''
Python's simplicity and readability make it a popular choice for many applications, but its interpreted nature can lead to performance challenges. Let's explore practical techniques for making your Python code faster.

## Understanding Performance Bottlenecks

### Profiling Your Code
Before optimizing, identify where time is actually spent:

```python
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result
```

### Line-by-Line Profiling
```python
# Using line_profiler
@profile
def slow_function():
    data = []
    for i in range(10000):
        data.append(i ** 2)  # This line might be slow
    return data
```

## Algorithmic Optimizations

### Choose the Right Data Structures
```python
# Slow: Using list for membership testing
slow_lookup = []
if item in slow_lookup:  # O(n) operation
    pass

# Fast: Using set for membership testing
fast_lookup = set()
if item in fast_lookup:  # O(1) operation
    pass
```

### List Comprehensions vs Loops
```python
# Slower
result = []
for i in range(1000):
    if i % 2 == 0:
        result.append(i ** 2)

# Faster
result = [i ** 2 for i in range(1000) if i % 2 == 0]

# Even faster for simple operations
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(1000))))
```

### Generator Expressions for Memory Efficiency
```python
# Memory intensive
squares = [x ** 2 for x in range(1000000)]

# Memory efficient
squares = (x ** 2 for x in range(1000000))
```

## NumPy for Numerical Operations

### Vectorization
```python
import numpy as np

# Slow: Pure Python loop
def slow_sum(arr):
    total = 0
    for item in arr:
        total += item ** 2
    return total

# Fast: NumPy vectorization
def fast_sum(arr):
    np_arr = np.array(arr)
    return np.sum(np_arr ** 2)
```

### Broadcasting
```python
# Efficient element-wise operations
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = arr1 * arr2  # Element-wise multiplication
```

## Caching and Memoization

### Function Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Simulate expensive computation
    result = 0
    for i in range(n):
        result += i ** 2
    return result
```

### Custom Caching
```python
class MemoizedFunction:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        
        result = self.func(*args)
        self.cache[args] = result
        return result

@MemoizedFunction
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Concurrent Programming

### Threading for I/O-Bound Tasks
```python
import concurrent.futures
import requests

def fetch_url(url):
    response = requests.get(url)
    return response.status_code

urls = ['http://example.com'] * 100

# Sequential
results = [fetch_url(url) for url in urls]

# Concurrent
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
```

### Multiprocessing for CPU-Bound Tasks
```python
import multiprocessing

def cpu_intensive_task(n):
    return sum(i ** 2 for i in range(n))

if __name__ == '__main__':
    numbers = [100000] * 8
    
    # Sequential
    results = [cpu_intensive_task(n) for n in numbers]
    
    # Parallel
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_intensive_task, numbers)
```

## Advanced Optimization Techniques

### Using Cython
```python
# fibonacci.pyx
def fib_cython(int n):
    cdef int a = 0
    cdef int b = 1
    cdef int i
    
    for i in range(n):
        a, b = b, a + b
    
    return a
```

### NumPy C Extensions
```python
import numpy as np
from numba import jit

@jit(nopython=True)
def fast_matrix_multiply(a, b):
    return np.dot(a, b)
```

### Memory Optimization
```python
# Use __slots__ to reduce memory usage
class OptimizedClass:
    __slots__ = ['x', 'y', 'z']
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
```

## Profiling Tools and Techniques

### Memory Profiling
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    data = [i for i in range(1000000)]
    return data
```

### Performance Benchmarking
```python
import timeit

def benchmark_function(func, *args, number=1000):
    return timeit.timeit(lambda: func(*args), number=number)

# Compare different implementations
time1 = benchmark_function(slow_function)
time2 = benchmark_function(fast_function)
print(f"Speedup: {time1/time2:.2f}x")
```

## Database Query Optimization

### Django ORM Optimization
```python
# Inefficient: N+1 queries
for user in User.objects.all():
    print(user.profile.bio)

# Efficient: Single query with select_related
for user in User.objects.select_related('profile'):
    print(user.profile.bio)

# Efficient: Bulk operations
User.objects.bulk_create([
    User(name=f'User {i}') for i in range(1000)
])
```

### Raw SQL When Needed
```python
from django.db import connection

def custom_query():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.name, COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            GROUP BY u.id
            ORDER BY post_count DESC
            LIMIT 10
        """)
        return cursor.fetchall()
```

Python performance optimization is about making informed decisions based on actual measurements. Profile first, optimize strategically, and always measure the impact of your changes.
                ''',
                'tags': 'Python,Performance,Optimization,Profiling,Best Practices',
                'is_featured': False,
                'is_published': True,
                'created': datetime.now() - timedelta(days=38)
            }
        ]
        
        created_count = 0
        for post_data in blog_posts:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created blog post: {post.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} blog posts!')
        )

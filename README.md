# 🎨 Professional Portfolio Website

A modern, responsive Django portfolio website with advanced features including contact management, dynamic content, and professional email notifications.

[![Django](https://img.shields.io/badge/Django-4.2.11-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### 🎯 **Core Features**
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Professional Dashboard**: Complete admin interface for content management
- **Contact System**: Advanced contact form with email notifications
- **Dynamic Content**: Projects, blog posts, testimonials, and more
- **SEO Optimized**: Meta tags, sitemaps, and search engine friendly

### 📧 **Email System**
- **Gmail Integration**: Professional email notifications to your mobile
- **Auto-Reply**: Automated thank you messages to visitors
- **Professional Templates**: Branded emails with your personal information
- **Mobile Notifications**: Instant Gmail notifications on your phone

### 🛡️ **Security Features**
- **Environment Variables**: Secure credential management
- **CSRF Protection**: Built-in Django security features
- **Input Validation**: Comprehensive form validation
- **Spam Protection**: Honeypot fields and rate limiting ready

### 📱 **Dashboard Features**
- **Message Management**: View, filter, search, and manage contact messages
- **Content Management**: Add/edit projects, blog posts, skills, education
- **Personal Information**: Update your profile and contact details
- **Media Management**: Upload and manage images and files

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Git
- Gmail account (for email notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to see your portfolio!

## 📧 Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account Settings → Security
   - Click "App passwords" 
   - Select "Mail" and "Other (Custom name)"
   - Enter "Portfolio Website"
   - Save the 16-character password

3. **Update .env file**:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   CONTACT_EMAIL=your-email@gmail.com
   ```

4. **Test email setup**:
   ```bash
   python manage.py test_email
   ```

## 🌐 Deployment

### Quick Deployment Options

#### Option 1: DigitalOcean App Platform (Recommended)
```bash
# 1. Connect GitHub repository
# 2. Set environment variables in dashboard
# 3. Deploy automatically
```

#### Option 2: Heroku
```bash
# 1. Install Heroku CLI
# 2. Create app: heroku create your-portfolio
# 3. Set environment variables: heroku config:set KEY=value
# 4. Deploy: git push heroku main
```

#### Option 3: VPS/Cloud Server
```bash
# 1. Set up server with Python and web server
# 2. Configure nginx + gunicorn
# 3. Set up SSL certificates
# 4. Configure environment variables
```

### Deployment Preparation

Run the deployment preparation script:
```bash
python deploy_prep.py
```

This will:
- Generate a secure production secret key
- Create production environment template
- Verify security configurations
- Create deployment documentation

See `DEPLOYMENT_README.md` for detailed deployment instructions.

## 📋 Environment Variables

### Required Variables
```env
SECRET_KEY=your-django-secret-key
DEBUG=False  # Set to False in production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=your-email@gmail.com
```

### Optional Variables
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🛠️ Development

### Project Structure
```
portfolio/
├── portfolio/              # Main Django app
├── dashboard/              # Admin dashboard app
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploaded files
├── portfolio_project/      # Django project settings
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

### Available Management Commands
```bash
python manage.py test_email          # Test email configuration
python manage.py collectstatic       # Collect static files
python manage.py migrate             # Apply database migrations
python manage.py createsuperuser     # Create admin user
```

### Running Tests
```bash
python manage.py test
```

## 📱 Features Overview

### 🏠 Homepage
- Hero section with your introduction
- Featured projects showcase
- Skills and expertise display
- Client testimonials
- Contact form

### 📂 Projects Section
- Project portfolio with filtering
- Detailed project pages
- GitHub integration
- Technology stack display
- Live demo links

### 📝 Blog (Optional)
- Article writing and publishing
- Tag-based categorization
- Featured posts
- SEO optimization

### 🎓 About Page
- Professional biography
- Education and certifications
- Career timeline
- Skills and expertise
- Downloadable resume

### 📞 Contact System
- Professional contact form
- Email notifications
- Auto-reply messages
- Dashboard message management
- Spam protection

### 🔧 Dashboard
- Content management interface
- Message management
- Personal information updates
- File uploads
- Site configuration

## 🎨 Customization

### Styling
- Bootstrap 5 framework
- Custom CSS in `static/css/`
- Responsive design
- Modern UI components

### Content Management
- Admin dashboard for all content
- Easy text and image updates
- Dynamic page generation
- SEO-friendly URLs

### Email Templates
- Professional branded emails
- Mobile-optimized formatting
- Personal information integration
- Customizable auto-replies

## 🔧 Technical Details

### Technologies Used
- **Backend**: Django 4.2.11, Python 3.9+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (dev), PostgreSQL/MySQL (prod)
- **Email**: SMTP (Gmail, SendGrid, etc.)
- **Hosting**: DigitalOcean, Heroku, VPS compatible

### Performance Features
- WhiteNoise for static file serving
- Django Compressor for CSS/JS optimization
- Database query optimization
- Caching ready
- SEO optimization

### Security Features
- CSRF protection
- XSS protection
- SQL injection protection
- Secure headers configuration
- Environment variable management

## 📞 Support

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Deployment Guide](DEPLOYMENT_README.md)

### Troubleshooting
- Check error logs in the console
- Verify environment variables
- Test email configuration
- Check database connections

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive framework
- Contributors and testers

---

**🚀 Ready to showcase your professional portfolio to the world!**

For deployment help, see [DEPLOYMENT_README.md](DEPLOYMENT_README.md)

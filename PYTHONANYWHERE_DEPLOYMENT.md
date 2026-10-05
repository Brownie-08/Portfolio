# PythonAnywhere Deployment Guide

This project is now configured for PythonAnywhere with SQLite.

## 1. Push or upload the project

Recommended path on PythonAnywhere:

```bash
/home/yourusername/My-Porfolio
```

If using GitHub:

```bash
cd ~
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git My-Porfolio
cd My-Porfolio
```

If uploading manually, upload the project folder contents to `/home/yourusername/My-Porfolio`.

## 2. Create the virtual environment

Use the same Python family as `runtime.txt` where possible.

```bash
cd /home/yourusername/My-Porfolio
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Create `.env` on PythonAnywhere

Create `/home/yourusername/My-Porfolio/.env` with real values:

```env
DEBUG=False
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
USE_CLOUDINARY=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

For a custom domain, use:

```env
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://yourusername.pythonanywhere.com
```

Do not commit `.env`.

## 4. Prepare SQLite and static files

```bash
cd /home/yourusername/My-Porfolio
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

The database file is `/home/yourusername/My-Porfolio/db.sqlite3`.

## 5. Configure PythonAnywhere Web tab

1. Go to the PythonAnywhere Web tab.
2. Add a new web app.
3. Choose Manual configuration.
4. Choose Python 3.11 if available.
5. Set Source code to:

```text
/home/yourusername/My-Porfolio
```

6. Set Working directory to:

```text
/home/yourusername/My-Porfolio
```

7. Set Virtualenv to:

```text
/home/yourusername/My-Porfolio/.venv
```

8. Open the WSGI configuration file and replace its contents with:

```python
import os
import sys

project_home = '/home/yourusername/My-Porfolio'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 6. Configure static and media mappings

In the Web tab Static files section, add:

```text
/static/  ->  /home/yourusername/My-Porfolio/staticfiles
/media/   ->  /home/yourusername/My-Porfolio/media
```

## 7. Reload and verify

Click Reload on the Web tab, then visit:

```text
https://yourusername.pythonanywhere.com/
https://yourusername.pythonanywhere.com/admin/
https://yourusername.pythonanywhere.com/static/css/styles.css
```

## 8. Manual data setup

Log into `/admin/` and add or review:

- Personal Information, including profile image and resume
- Skills
- Projects
- Education
- Career Timeline / Experience
- Certifications
- Awards
- Testimonials
- SEO Settings
- Footer Links
- Blog Posts

Uploads should appear under `/media/` and persist on PythonAnywhere storage.

## 9. Updating after future code changes

```bash
cd /home/yourusername/My-Porfolio
source .venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click Reload on the PythonAnywhere Web tab.

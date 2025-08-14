release: python manage.py migrate --noinput
web: gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT

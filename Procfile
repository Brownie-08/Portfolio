release: python manage.py migrate --noinput --settings=portfolio_project.settings.railway
web: gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT

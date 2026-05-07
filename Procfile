web: gunicorn -c gunicorn.conf.py setup.wsgi:application
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput

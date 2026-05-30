web: python manage.py migrate --noinput && python manage.py ensure_platform_seed && gunicorn core.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate --noinput && python manage.py ensure_platform_seed

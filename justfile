dev:
    echo $DEBUG
    echo $DATABASE_URL
    python manage.py runserver 0.0.0.0:8001
serve:
    echo $DEBUG
    echo $DATABASE_URL
    gunicorn --bind 0.0.0.0:8001 --workers 2 ecomm.wsgi:application

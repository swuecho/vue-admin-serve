## superuser


## install dev

```
pip install -r requirements.txt
```

## setup dev env var
```
export DEBUG=1
export DATABASE_URL=pg_url
```


## start server

python manage.py makemigrations admin_backend

python manage.py migrate

```
python manage.py runserver 0.0.0.0:8001
```

## reset sequence

python manage.py sqlsequencereset admin_backend

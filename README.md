
## frontend

https://github.com/swuecho/vue-admin-ui

## install dev

```
pip install -r requirements.txt
```

## setup dev env var
```
export DEBUG=1
export DATABASE_URL=pg_url
```

## run migration

```sh
#python manage.py makemigrations admin_backend
python manage.py migrate
```

## create data

1. create admin user

```bash
python manage.py createsuperuser
```

2. add permission data

```sh
python manage.py loaddata data/permission.json 
python manage.py loaddata data/role.json 
python manage.py loaddata data/user_roles_role.json
python manage.py loaddata admin_backend.rolepermissionspermission 
```

## start server


```
python manage.py runserver 0.0.0.0:8001
```

## reset sequence

python manage.py sqlsequencereset admin_backend







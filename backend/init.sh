#!/bin/sh

until nc -z -v -w30 "db" 5432
do
  echo "Waiting for Postgres to up..."
  sleep 2
done

crond
python manage.py installtasks
python manage.py collectstatic --noinput
python manage.py migrate

gunicorn marker.wsgi:application

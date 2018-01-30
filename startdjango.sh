#!/bin/sh

python /superlists/sec_key_gen.py

python /superlists/manage.py migrate

#python /superlists/manage.py runserver 0.0.0.0:8000 &

cd /superlists && gunicorn --bind unix:/var/run/gunicorn.socket superlists.wsgi:application &

nginx -g "daemon off;"

#!/bin/sh

python /superlists/vault_client_token.py

python /superlists/manage.py migrate

python /superlists/manage.py runserver 0.0.0.0:8000 &

cd /superlists && gunicorn --bind 0.0.0.0:8000 superlists.wsgi:application &

nginx -g "daemon off;"

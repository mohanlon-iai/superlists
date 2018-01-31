FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && \
	apk add nginx
	
RUN mkdir -p /run/nginx

COPY nginx.conf /etc/nginx/

RUN mkdir /superlists

WORKDIR /superlists

COPY requirements.txt /superlists/

RUN pip install -r requirements.txt

COPY . dcos-config/* /superlists/

RUN echo -e '#!/bin/sh \n\
python /superlists/vault_sec_key.py \n\
python /superlists/manage.py collectstatic --noinput \n\
python /superlists/manage.py migrate \n\
cd /superlists && gunicorn --bind unix:/var/run/gunicorn.socket superlists.wsgi:application & \n\
nginx -g "daemon off;"' >> entrypoint.sh

EXPOSE 80

RUN chmod 550 entrypoint.sh

ENTRYPOINT ["/superlists/entrypoint.sh"]

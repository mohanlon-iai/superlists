FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && \
	apk add nginx
	
RUN mkdir -p /run/nginx

COPY nginx.conf /etc/nginx/

RUN mkdir /superlists

WORKDIR /superlists

ADD requirements.txt /superlists/

RUN pip install -r requirements.txt

ADD . /superlists/

RUN python -c "import random; print(''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)))" >> sec_key && python /superlists/manage.py collectstatic --noinput

RUN rm sec_key

EXPOSE 80

CMD ["sh", "/superlists/startdjango.sh"]

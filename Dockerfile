FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /superlists

WORKDIR /superlists

ADD requirements.txt /superlists/

RUN pip install -r requirements.txt

ADD . /superlists/

EXPOSE 8000

CMD ["sh", "/superlists/startdjango.sh"]

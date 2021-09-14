FROM tiangolo/meinheld-gunicorn:python3.8-alpine3.11

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./app /app

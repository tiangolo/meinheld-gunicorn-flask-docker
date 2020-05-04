FROM tiangolo/meinheld-gunicorn:python2.7

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install flask

COPY ./app /app

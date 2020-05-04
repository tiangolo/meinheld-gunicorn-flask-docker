FROM tiangolo/meinheld-gunicorn:python3.6

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install flask

COPY ./app /app

FROM tiangolo/meinheld-gunicorn:python3.9-alpine3.13

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install flask

COPY ./app /app

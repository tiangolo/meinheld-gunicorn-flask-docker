FROM tiangolo/meinheld-gunicorn:python3.9

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install flask

COPY ./app /app

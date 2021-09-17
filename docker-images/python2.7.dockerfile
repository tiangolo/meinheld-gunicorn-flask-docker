FROM tiangolo/meinheld-gunicorn:python2.7

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# Install requirements
# Newer versions don't support Python 2.7 (Python 2.7 reached end of life long ago)
# So for this tag just install whatever is available for Python 2.7, don't use
# Dependabot's updated requirements
RUN pip install --no-cache-dir flask

COPY ./app /app

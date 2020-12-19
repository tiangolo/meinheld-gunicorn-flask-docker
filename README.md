[![Test](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/workflows/Test/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions?query=workflow%3ATest) [![Deploy](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/workflows/Deploy/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions?query=workflow%3ADeploy)

## Supported tags and respective `Dockerfile` links

* [`python3.8`, `latest` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.8.dockerfile)
* [`python3.8-alpine3.11` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.8-alpine3.11.dockerfile)
* [`python3.7`, _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.7.dockerfile)
* [`python3.7-alpine3.8` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.7-alpine3.8.dockerfile)
* [`python3.6` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.6.dockerfile)
* [`python3.6-alpine3.8` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.6-alpine3.8.dockerfile)
* [`python2.7` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python2.7.dockerfile)

**Note**: Note: There are [tags for each build date](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/tags). If you need to "pin" the Docker image version you use, you can select one of those tags. E.g. `tiangolo/meinheld-gunicorn-flask:python3.7-2019-10-15`.

# meinheld-gunicorn-flask

[**Docker**](https://www.docker.com/) image with [**Meinheld**](http://meinheld.org/) managed by [**Gunicorn**](https://gunicorn.org/) for high-performance web applications in [**Flask**](http://flask.pocoo.org/) using **[Python](https://www.python.org/) 3.6** and above and **Python 2.7**, with performance auto-tuning. Optionally with Alpine Linux.

**GitHub repo**: [https://github.com/tiangolo/meinheld-gunicorn-flask-docker](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)

**Docker Hub image**: [https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/)

## Description

Python Flask web applications running with **Meinheld** controlled by **Gunicorn** have some of the [best performances achievable by Flask](https://www.techempower.com/benchmarks/#section=test&runid=a979de55-980d-4721-a46f-77298b3f3923&hw=ph&test=fortune&l=zijzen-7) (*).

If you have an already existing application in Flask or are building a new one, this image will give you the best performance possible (or close to that).

This image has an "auto-tuning" mechanism included, so that you can just add your code and get **good performance** automatically. And without making sacrifices (like logging).

### * Note on performance and features

If you are starting a new project, you might benefit from a newer and faster framework like [**FastAPI**](https://github.com/tiangolo/fastapi) (based on ASGI instead of WSGI like Flask and Django), and a Docker image like [**tiangolo/uvicorn-gunicorn-fastapi**](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker).

It would give you about 200% the performance achievable with Flask, even when using this image.

Also, if you want to use new technologies like WebSockets it would be easier with a newer framework based on ASGI, like **FastAPI**. As the standard ASGI was designed to be able to handle asynchronous code like the one needed for WebSockets.

## Technical Details

### Meinheld

**Meinheld** is a high-performance WSGI-compliant web server.

### Gunicorn

You can use **Gunicorn** to manage Meinheld and run multiple processes of it.

### Flask

Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

## Alternatives

This image was created to be an alternative to [**tiangolo/uwsgi-nginx-flask**](https://github.com/tiangolo/uwsgi-nginx-flask-docker), providing about 400% the performance of that image.

It is based on the more generic image [**tiangolo/meinheld-gunicorn**](https://github.com/tiangolo/meinheld-gunicorn-docker). That's the one you would use for other WSGI frameworks, like Django.

## How to use

* You don't need to clone the GitHub repo. You can use this image as a base image for other images, using this in your `Dockerfile`:

```Dockerfile
FROM tiangolo/meinheld-gunicorn-flask:python3.7

COPY ./app /app
```

It will expect a file at `/app/app/main.py`.

Or otherwise a file at `/app/main.py`.

And will expect it to contain a variable `app` with your "WSGI" application.

Then you can build your image from the directory that has your `Dockerfile`, e.g:

```bash
docker build -t myimage ./
```

## Advanced usage

### Environment variables

These are the environment variables that you can set in the container to configure it and their default values:

#### `MODULE_NAME`

The Python "module" (file) to be imported by Gunicorn, this module would contain the actual Flask application in a variable.

By default:

* `app.main` if there's a file `/app/app/main.py` or
* `main` if there's a file `/app/main.py`

For example, if your main file was at `/app/custom_app/custom_main.py`, you could set it like:

```bash
docker run -d -p 80:80 -e MODULE_NAME="custom_app.custom_main" myimage
```

#### `VARIABLE_NAME`

The variable inside of the Python module that contains the Flask application.

By default:

* `app`

For example, if your main Python file has something like:

```Python
from flask import Flask
api = Flask(__name__)

@api.route("/")
def hello():
    return "Hello World from Flask"
```

In this case `api` would be the variable with the "Flask application". You could set it like:

```bash
docker run -d -p 80:80 -e VARIABLE_NAME="api" myimage
```

#### `APP_MODULE`

The string with the Python module and the variable name passed to Gunicorn.

By default, set based on the variables `MODULE_NAME` and `VARIABLE_NAME`:

* `app.main:app` or
* `main:app`

You can set it like:

```bash
docker run -d -p 80:80 -e APP_MODULE="custom_app.custom_main:api" myimage
```

#### `GUNICORN_CONF`

The path to a Gunicorn Python configuration file.

By default:

* `/app/gunicorn_conf.py` if it exists
* `/app/app/gunicorn_conf.py` if it exists
* `/gunicorn_conf.py` (the included default)

You can set it like:

```bash
docker run -d -p 80:80 -e GUNICORN_CONF="/app/custom_gunicorn_conf.py" myimage
```

#### `WORKERS_PER_CORE`

This image will check how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

By default:

* `2`

You can set it like:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="3" myimage
```

If you used the value `3` in a server with 2 CPU cores, it would run 6 worker processes.

You can use floating point values too.

So, for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have an ASGI application that you know won't need high performance. And you don't want to waste server resources. You could make it use `0.5` workers per CPU core. For example:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="0.5" myimage
```

In a server with 8 CPU cores, this would make it start only 4 worker processes.

#### `WEB_CONCURRENCY`

Override the automatic definition of number of workers.

By default:

* Set to the number of CPU cores in the current server multiplied by the environment variable `WORKERS_PER_CORE`. So, in a server with 2 cores, by default it will be set to `4`.

You can set it like:

```bash
docker run -d -p 80:80 -e WEB_CONCURRENCY="2" myimage
```

This would make the image start 2 worker processes, independent of how many CPU cores are available in the server.

#### `HOST`

The "host" used by Gunicorn, the IP where Gunicorn will listen for requests.

It is the host inside of the container.

So, for example, if you set this variable to `127.0.0.1`, it will only be available inside the container, not in the host running it.

It's is provided for completeness, but you probably shouldn't change it.

By default:

* `0.0.0.0`

#### `PORT`

The port the container should listen on.

If you are running your container in a restrictive environment that forces you to use some specific port (like `8080`) you can set it with this variable.

By default:

* `80`

You can set it like:

```bash
docker run -d -p 80:8080 -e PORT="8080" myimage
```

#### `BIND`

The actual host and port passed to Gunicorn.

By default, set based on the variables `HOST` and `PORT`.

So, if you didn't change anything, it will be set by default to:

* `0.0.0.0:80`

You can set it like:

```bash
docker run -d -p 80:8080 -e BIND="0.0.0.0:8080" myimage
```

#### `LOG_LEVEL`

The log level for Gunicorn.

One of:

* `debug`
* `info`
* `warning`
* `error`
* `critical`

By default, set to `info`.

If you need to squeeze more performance sacrificing logging, set it to `warning`, for example:

You can set it like:

```bash
docker run -d -p 80:8080 -e LOG_LEVEL="warning" myimage
```

Logs are sent to the container's `stderr` and `stdout`, meaning you can view the logs with the `docker logs -f your_container_name_here` command.

### Custom Gunicorn configuration file

The image includes a default Gunicorn Python config file at `/gunicorn_conf.py`.

It uses the environment variables declared above to set all the configurations.

You can override it by including a file in:

* `/app/gunicorn_conf.py`
* `/app/app/gunicorn_conf.py`
* `/gunicorn_conf.py`

### Custom `/app/prestart.sh`

If you need to run anything before starting the app, you can add a file `prestart.sh` to the directory `/app`. The image will automatically detect and run it before starting everything.

For example, if you want to add Alembic SQL migrations (with SQLALchemy), you could create a `./app/prestart.sh` file in your code directory (that will be copied by your `Dockerfile`) with:

```bash
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
```

and it would wait 10 seconds to give the database some time to start and then run that `alembic` command.

If you need to run a Python script before starting the app, you could make the `/app/prestart.sh` file run your Python script, with something like:

```bash
#! /usr/bin/env bash

# Run custom Python script before starting
python /app/my_custom_prestart_script.py
```

## Tests

All the image tags, configurations, environment variables and application options are tested.

## Release Notes

### Latest Changes

* 🎨 Format GitHub Action latest-changes. PR [#42](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/42) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action latest-changes, update issue-manager, add funding. PR [#41](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/41) by [@tiangolo](https://github.com/tiangolo).
* Add Python 3.8 with Alpine 3.11. PR [#28](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/28).
* Fix typo in README. PR [#18](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/18) by [@tahmid-choyon](https://github.com/tahmid-choyon).
* Add support for Python 3.8. PR [#27](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/27).
* Refactor build setup:
    * Use GitHub actions for CI.
    * Simplify, centralize, and deduplicate code and configs.
    * Update tests.
    * Move from Pipenv to Poetry.
    * PR [#26](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/26).

### 0.3.0

* Refactor tests to use env vars and add image tags for each build date, like `tiangolo/meinheld-gunicorn-flask:python3.7-2019-10-15`. PR [#17](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/17).

### 0.2.0

* Add support for Python 2.7 (you should use Python 3.7 or Python 3.6). PR [#11](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/11).

* Update Travis CI configuration. PR [#10](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/10) by [@cclauss](https://github.com/cclauss).

### 0.1.0

* Add support for `/app/prestart.sh`.

## License

This project is licensed under the terms of the MIT license.

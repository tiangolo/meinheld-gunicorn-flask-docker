[![Test](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/workflows/Test/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions?query=workflow%3ATest) [![Deploy](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/workflows/Deploy/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions?query=workflow%3ADeploy)

## Supported tags and respective `Dockerfile` links

* [`python3.9`, `latest` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.9.dockerfile)
* [`python3.8`, _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.8.dockerfile)
* [`python3.7`, _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.7.dockerfile)
* [`python3.6` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.6.dockerfile)

## Discouraged tags

* [`python3.9-alpine3.13` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.9-alpine3.13.dockerfile)
* [`python3.8-alpine3.11` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.8-alpine3.11.dockerfile)
* [`python3.7-alpine3.8` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.7-alpine3.8.dockerfile)
* [`python3.6-alpine3.8` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.6-alpine3.8.dockerfile)

To learn more about why Alpine images are discouraged for Python read the note at the end: [🚨 Alpine Python Warning](#-alpine-python-warning).

## Deprecated

These tags are no longer supported:

* [`python2.7` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python2.7.dockerfile)

---

**Note**: There are [tags for each build date](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/tags). If you need to "pin" the Docker image version you use, you can select one of those tags. E.g. `tiangolo/meinheld-gunicorn-flask:python3.7-2019-10-15`.

# meinheld-gunicorn-flask

[**Docker**](https://www.docker.com/) image with [**Meinheld**](http://meinheld.org/) managed by [**Gunicorn**](https://gunicorn.org/) for high-performance web applications in [**Flask**](http://flask.pocoo.org/) using **[Python](https://www.python.org/)** with performance auto-tuning. Optionally with Alpine Linux.

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

## 🚨 WARNING: You Probably Don't Need this Docker Image

You are probably using **Kubernetes** or similar tools. In that case, you probably **don't need this image** (or any other **similar base image**). You are probably better off **building a Docker image from scratch**.

---

If you have a cluster of machines with **Kubernetes**, Docker Swarm Mode, Nomad, or other similar complex system to manage distributed containers on multiple machines, then you will probably want to **handle replication** at the **cluster level** instead of using a **process manager** in each container that starts multiple **worker processes**, which is what this Docker image does.

In those cases (e.g. using Kubernetes) you would probably want to build a **Docker image from scratch**, installing your dependencies, and running **a single process** instead of this image.

For example, using [Gunicorn](https://gunicorn.org/) you could have a file `app/gunicorn_conf.py` with:

```Python
# Gunicorn config variables
loglevel = "info"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 5
threads = 3
```

And then you could have a `Dockerfile` with:

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["gunicorn", "--conf", "app/gunicorn_conf.py", "--bind", "0.0.0.0:80", "app.main:app"]
```

You can read more about these ideas in the [FastAPI documentation about: FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes) as the same ideas would apply to other web applications in containers.

## When to Use this Docker Image

### A Simple App

You could want a process manager running multiple worker processes in the container if your application is **simple enough** that you don't need (at least not yet) to fine-tune the number of processes too much, and you can just use an automated default, and you are running it on a **single server**, not a cluster.

### Docker Compose

You could be deploying to a **single server** (not a cluster) with **Docker Compose**, so you wouldn't have an easy way to manage replication of containers (with Docker Compose) while preserving the shared network and **load balancing**.

Then you could want to have **a single container** with a **process manager** starting **several worker processes** inside, as this Docker image does.

### Prometheus and Other Reasons

You could also have **other reasons** that would make it easier to have a **single container** with **multiple processes** instead of having **multiple containers** with **a single process** in each of them.

For example (depending on your setup) you could have some tool like a Prometheus exporter in the same container that should have access to **each of the requests** that come.

In this case, if you had **multiple containers**, by default, when Prometheus came to **read the metrics**, it would get the ones for **a single container each time** (for the container that handled that particular request), instead of getting the **accumulated metrics** for all the replicated containers.

Then, in that case, it could be simpler to have **one container** with **multiple processes**, and a local tool (e.g. a Prometheus exporter) on the same container collecting Prometheus metrics for all the internal processes and exposing those metrics on that single container.

---

Read more about it all in the [FastAPI documentation about: FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/), as the same concepts apply to other web applications in containers.

## How to use

You don't have to clone this repo.

You can use this image as a base image for other images.

Assuming you have a file `requirements.txt`, you could have a `Dockerfile` like this:

```Dockerfile
FROM tiangolo/meinheld-gunicorn-flask:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

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

## 🚨 Alpine Python Warning

In short: You probably shouldn't use Alpine for Python projects, instead use the `slim` Docker image versions.

---

Do you want more details? Continue reading 👇

Alpine is more useful for other languages where you build a static binary in one Docker image stage (using multi-stage Docker building) and then copy it to a simple Alpine image, and then just execute that binary. For example, using Go.

But for Python, as Alpine doesn't use the standard tooling used for building Python extensions, when installing packages, in many cases Python (`pip`) won't find a precompiled installable package (a "wheel") for Alpine. And after debugging lots of strange errors you will realize that you have to install a lot of extra tooling and build a lot of dependencies just to use some of these common Python packages. 😩

This means that, although the original Alpine image might have been small, you end up with a an image with a size comparable to the size you would have gotten if you had just used a standard Python image (based on Debian), or in some cases even larger. 🤯

And in all those cases, it will take much longer to build, consuming much more resources, building dependencies for longer, and also increasing its carbon footprint, as you are using more CPU time and energy for each build. 🌳

If you want slim Python images, you should instead try and use the `slim` versions that are still based on Debian, but are smaller. 🤓

## Tests

All the image tags, configurations, environment variables and application options are tested.

## Release Notes

### Latest Changes

* 🔥 Remove support for Python 2.7. PR [#63](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/63) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add Kubernetes warning, when to use this image. PR [#62](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/62) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo duplicate "Note" in Readme. PR [#61](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/61) by [@tiangolo](https://github.com/tiangolo).
* ♻ Refactor dependencies to improve Dependabot updates and reduce disk size used. PR [#60](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/60) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Latest Changes GitHub Action. PR [#59](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/59) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add Dependabot and external dependencies to get automated upgrade PRs. PR [#51](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/51) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add support for Python 3.9 and Python 3.9 Alpine. PR [#50](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/50) by [@tiangolo](https://github.com/tiangolo).
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

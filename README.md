[![Test](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions/workflows/test.yml/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions/workflows/test.yml) [![Deploy](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/workflows/Deploy/badge.svg)](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/actions?query=workflow%3ADeploy)

## Supported tags and respective `Dockerfile` links

* [`python3.9`, `latest` _(Dockerfile)_](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/docker-images/python3.9.dockerfile)

## Deprecated tags

🚨 These tags are no longer supported or maintained, they are removed from the GitHub repository, but the last versions pushed might still be available in Docker Hub if anyone has been pulling them:

* `python3.9-alpine3.13`
* `python3.8`
* `python3.8-alpine3.11`
* `python3.7`
* `python3.7-alpine3.8`
* `python3.6`
* `python3.6-alpine3.8`
* `python2.7`

The last date tags for these versions are:

* `python3.9-alpine3.13-2024-03-11`
* `python3.8-2024-10-28`
* `python3.8-alpine3.11-2024-03-11`
* `python3.7-2024-10-28`
* `python3.7-alpine3.8-2024-03-11`
* `python3.6-2022-11-25`
* `python3.6-alpine3.8-2022-11-25`
* `python2.7-2022-11-25`

---

**Note**: There are [tags for each build date](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/tags). If you need to "pin" the Docker image version you use, you can select one of those tags. E.g. `tiangolo/meinheld-gunicorn-flask:python3.9-2024-11-02`.

# meinheld-gunicorn-flask

[**Docker**](https://www.docker.com/) image with [**Meinheld**](http://meinheld.org/) managed by [**Gunicorn**](https://gunicorn.org/) for high-performance web applications in [**Flask**](http://flask.pocoo.org/) using **[Python](https://www.python.org/)** with performance auto-tuning.

**GitHub repo**: [https://github.com/tiangolo/meinheld-gunicorn-flask-docker](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)

**Docker Hub image**: [https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/)

## Description

Python Flask web applications running with **Meinheld** controlled by **Gunicorn** have some of the [best performances achievable by Flask](https://www.techempower.com/benchmarks/#section=test&runid=a979de55-980d-4721-a46f-77298b3f3923&hw=ph&test=fortune&l=zijzen-7) (*).

If you have an already existing application in Flask or are building a new one, this image will give you the best performance possible (or close to that).

This image has an "auto-tuning" mechanism included, so that you can just add your code and get **good performance** automatically. And without making sacrifices (like logging).

## Note Python 3.10 and 3.11

The current latest version of Meinheld released is 1.0.2, from May 17, 2020. This version of Meinheld requires an old version of Greenlet (`>=0.4.5,<0.5`) that is not compatible with Python 3.10 and 3.11. That's why the latest version of Python supported in this image is Python 3.9.

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

#### Upgrades

* ⬆ Bump flask from 3.1.0 to 3.1.1. PR [#169](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/169) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump flask from 3.0.3 to 3.1.0. PR [#167](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/167) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump flask from 2.2.5 to 3.0.3. PR [#147](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/147) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Drop support for Python 3.7 and 3.8. PR [#164](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/164) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump gunicorn from 22.0.0 to 23.0.0. PR [#152](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/152) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump gunicorn from 20.1.0 to 22.0.0. PR [#149](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/149) by [@dependabot[bot]](https://github.com/apps/dependabot).

#### Internal

* ⬆ Bump tiangolo/latest-changes from 0.3.1 to 0.3.2. PR [#166](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/166) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Remove old unused files. PR [#165](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/165) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/issue-manager from 0.5.0 to 0.5.1. PR [#163](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/163) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/build-push-action from 5 to 6. PR [#150](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/150) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update `issue-manager.yml`. PR [#154](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/154) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `latest-changes` GitHub Action. PR [#153](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/153) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update issue-manager.yml GitHub Action permissions. PR [#151](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/151) by [@tiangolo](https://github.com/tiangolo).
* Bump gunicorn from 20.1.0 to 22.0.0 in /docker-images. PR [#148](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/148) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/build-push-action from 2 to 5. PR [#144](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/144) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/setup-buildx-action from 1 to 3. PR [#143](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/143) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/login-action from 1 to 3. PR [#142](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/142) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 4 to 5. PR [#132](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/132) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump peter-evans/dockerhub-description from 3 to 4. PR [#130](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/130) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update black requirement from ^22.10 to ^23.3. PR [#120](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/120) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Add GitHub templates for discussions and issues, and security policy. PR [#146](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/146) by [@alejsdev](https://github.com/alejsdev).
* ⬆ Update mypy requirement from ^0.991 to ^1.4. PR [#136](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/136) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update `latest-changes.yml`. PR [#141](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/141) by [@alejsdev](https://github.com/alejsdev).

### 0.5.0

#### Features

* ✨ Add support for multiarch builds, including ARM (e.g. Mac M1). PR [#138](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/138) by [@tiangolo](https://github.com/tiangolo).

#### Refactor

* 🔥 Remove Alpine support. PR [#128](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/128) by [@tiangolo](https://github.com/tiangolo).

#### Upgrades

* ⬆️ Bump flask from 2.2.2 to 2.2.5 in /docker-images. PR [#129](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/129) by [@dependabot[bot]](https://github.com/apps/dependabot).

#### Docs

* 📝 Update test badge in `README.md`. PR [#137](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/137) by [@alejsdev](https://github.com/alejsdev).

#### Internal

* 🐛 Fix latest-changes GitHub Action, take 2. PR [#140](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/140) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/issue-manager from 0.4.0 to 0.5.0. PR [#131](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/131) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update dependabot. PR [#126](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/126) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update latest-changes GitHub Action. PR [#125](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/125) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix latest-changes GitHub Action. PR [#139](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/139) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update token for latest changes. PR [#124](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/124) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action for Docker Hub description. PR [#113](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/113) by [@tiangolo](https://github.com/tiangolo).

### 0.4.0

#### Features

Highlights of this release:

* Support for Python 3.9 and 3.8.
* Deprecation of Python 3.6 and 2.7.
    * The last Python 3.6 and 2.7 images are available in Docker Hub, but they won't be updated or maintained anymore.
    * The last images with a date tag are `python3.6-2022-11-25` and `python2.7-2022-11-25`.
* Upgraded versions of all the dependencies.
* Small improvements and fixes.

* ✨ Add support for Python 3.9 and Python 3.9 Alpine. PR [#50](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/50) by [@tiangolo](https://github.com/tiangolo).
* Add Python 3.8 with Alpine 3.11. PR [#28](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/28).
* Add support for Python 3.8. PR [#27](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/27).

#### Breaking Changes

* 🔥 Deprecate and remove Python 3.6 and 2.7. PR [#105](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/105) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove support for Python 2.7. PR [#63](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/63) by [@tiangolo](https://github.com/tiangolo).

#### Upgrades

* ⬆️ Bump flask from 2.0.1 to 2.2.2 in /docker-images. PR [#98](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/98) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Upgrade Flask to the latest version supporting Python 3.6. PR [#101](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/101) by [@tiangolo](https://github.com/tiangolo).

#### Docs

* 📝 Add note about Python 3.10 and 3.11. PR [#112](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/112) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add note to discourage Alpine with Python. PR [#64](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/64) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add Kubernetes warning, when to use this image. PR [#62](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/62) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo duplicate "Note" in Readme. PR [#61](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/61) by [@tiangolo](https://github.com/tiangolo).
* Fix typo in README. PR [#18](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/18) by [@tahmid-choyon](https://github.com/tahmid-choyon).

#### Internal

* ⬆️ Update autoflake requirement from ^1.3.1 to ^2.0.0. PR [#110](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/110) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update black requirement from ^20.8b1 to ^22.10. PR [#109](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/109) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update mypy requirement from ^0.971 to ^0.991. PR [#108](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/108) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update docker requirement from ^5.0.3 to ^6.0.1. PR [#107](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/107) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Upgrade CI OS. PR [#111](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/111) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Dependabot config. PR [#106](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/106) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add scheduled CI. PR [#104](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/104) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add alls-green GitHub Action. PR [#103](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/103) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not run double CI for PRs, run on push only on master. PR [#102](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/102) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Update black requirement from ^19.10b0 to ^20.8b1. PR [#57](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/57) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update pytest requirement from ^5.4.1 to ^7.0.1. PR [#76](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/76) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump actions/checkout from 2 to 3.1.0. PR [#99](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/99) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update isort requirement from ^4.3.21 to ^5.8.0. PR [#55](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/55) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump tiangolo/issue-manager from 0.2.0 to 0.4.0. PR [#52](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/52) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update docker requirement from ^4.2.0 to ^5.0.3. PR [#66](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/66) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump actions/setup-python from 1 to 4. PR [#93](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/93) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update mypy requirement from ^0.770 to ^0.971. PR [#95](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/95) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Remove Travis backup file. PR [#67](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/67) by [@tiangolo](https://github.com/tiangolo).
* ♻ Refactor dependencies to improve Dependabot updates and reduce disk size used. PR [#60](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/60) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Latest Changes GitHub Action. PR [#59](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/59) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add Dependabot and external dependencies to get automated upgrade PRs. PR [#51](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/51) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Format GitHub Action latest-changes. PR [#42](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/42) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action latest-changes, update issue-manager, add funding. PR [#41](https://github.com/tiangolo/meinheld-gunicorn-flask-docker/pull/41) by [@tiangolo](https://github.com/tiangolo).
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

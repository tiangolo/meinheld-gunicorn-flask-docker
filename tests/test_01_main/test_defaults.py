import time

import pytest
import requests

import docker

from ..utils import CONTAINER_NAME, get_config, get_logs, remove_previous_container

client = docker.from_env()


def verify_container(container, response_text):
    config_data = get_config(container)
    assert config_data["workers_per_core"] == 2
    assert config_data["host"] == "0.0.0.0"
    assert config_data["port"] == "80"
    assert config_data["loglevel"] == "info"
    assert config_data["workers"] > 2
    assert config_data["bind"] == "0.0.0.0:80"
    logs = get_logs(container)
    assert "Checking for script in /app/prestart.sh" in logs
    assert "Running script /app/prestart.sh" in logs
    assert (
        "Running inside /app/prestart.sh, you could add migrations to this file" in logs
    )
    response = requests.get("http://127.0.0.1:8000")
    assert response.text == response_text


@pytest.mark.parametrize(
    "image,response_text",
    [
        (
            "tiangolo/meinheld-gunicorn-flask:python2.7",
            "Hello World from Flask in a Docker container running Python 2.7 with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn-flask:python3.6",
            "Hello World from Flask in a Docker container running Python 3.6 with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn-flask:python3.7",
            "Hello World from Flask in a Docker container running Python 3.7 with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn-flask:latest",
            "Hello World from Flask in a Docker container running Python 3.7 with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn-flask:python3.6-alpine3.8",
            "Hello World from Flask in a Docker container running Python 3.6 with Meinheld and Gunicorn on Alpine (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8",
            "Hello World from Flask in a Docker container running Python 3.7 with Meinheld and Gunicorn on Alpine (default)",
        ),
    ],
)
def test_defaults(image, response_text):
    remove_previous_container(client)
    container = client.containers.run(
        image, name=CONTAINER_NAME, ports={"80": "8000"}, detach=True
    )
    time.sleep(1)
    verify_container(container, response_text)
    container.stop()
    # Test that everything works after restarting too
    container.start()
    time.sleep(1)
    verify_container(container, response_text)
    container.stop()
    container.remove()

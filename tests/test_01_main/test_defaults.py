import time

import docker
import pytest
import requests

from ..utils import CONTAINER_NAME, get_config, stop_previous_container

client = docker.from_env()


@pytest.mark.parametrize(
    "image,response_text",
    [
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
    stop_previous_container(client)
    container = client.containers.run(
        image, name=CONTAINER_NAME, ports={"80": "8000"}, detach=True
    )
    time.sleep(1)
    config_data = get_config(container)
    assert config_data["workers_per_core"] == 2
    assert config_data["host"] == "0.0.0.0"
    assert config_data["port"] == "80"
    assert config_data["loglevel"] == "info"
    assert config_data["workers"] > 2
    assert config_data["bind"] == "0.0.0.0:80"
    response = requests.get("http://127.0.0.1:8000")
    assert response.text == response_text
    container.stop()
    container.remove()

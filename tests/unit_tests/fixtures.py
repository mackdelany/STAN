"""
"""

import json
import os
from pathlib import Path
import pytest

from stan.api import app


@pytest.fixture
def dev_client():
    os.environ["APP_CONFIG_FILE"] = str(
        Path().absolute()) + "/stan/api/config/development.py"
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    app.config['TESTING'] = True  # probably doesn't work ?
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture
def prod_client():
    os.environ["APP_CONFIG_FILE"] = str(
        Path().absolute()) + "/stan/api/config/production.py"
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    app.config['TESTING'] = True
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture
def prod_client_test():
    os.environ["APP_CONFIG_FILE"] = str(
        Path().absolute()) + "/stan/api/config/production.py"
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def prod_api_key():
    os.environ["APP_CONFIG_FILE"] = str(
        Path().absolute()) + "/stan/api/config/production.py"
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    prod_api_key = app.config['AUTH_KEYS']['TESTING']
    return prod_api_key


@pytest.fixture
def cennz_requests():
    with open("tests/unit_tests/cennz_unit_test_requests.json", "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def integration_requests():
    with open("tests/unit_tests/integration_test_requests.json", "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def warning_requests():
    with open("tests/unit_tests/warning_test_requests.json", "r") as read_file:
        return json.load(read_file)

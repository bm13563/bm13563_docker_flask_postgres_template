from os import environ

import pytest

from api.app import create_app


def pytest_configure(config):
    environ["DB_HOST"] = "localhost"


@pytest.fixture()
def app():
    app = create_app()
    yield app
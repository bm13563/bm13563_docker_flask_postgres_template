from os import environ


def pytest_configure(config):
    environ["DB_HOST"] = "localhost"

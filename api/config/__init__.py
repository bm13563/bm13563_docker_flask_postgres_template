from flask import g

from common.config import Config


def get_config():
    if "config" not in g:
        g.config = Config()
    return g.config


def get_config_value(name, default=None):
    return get_config().get(name, default)

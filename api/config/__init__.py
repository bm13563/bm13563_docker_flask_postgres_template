from flask import g

from api.config.config import Config


def get_config():
    if "config" not in g:
        g.config = Config()
    return g.config

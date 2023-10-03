from flask import g

from api.config import get_config
from common.db_manager import get_instanced_dbm


def get_dbm():
    if "dbm" not in g:
        config = get_config()
        g.dbm = get_instanced_dbm(config)
    return g.dbm

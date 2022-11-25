from flask import g

from api.config import get_config
from api.db.db_manager import DbManager


def get_dbm():
    if "dbm" not in g:
        config = get_config()
        g.dbm = DbManager(config)
    return g.dbm

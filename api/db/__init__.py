from flask import g

from api.db.db_manager import DbManager


def get_dbm():
    if "dbm" not in g:
        g.dbm = DbManager()
    return g.dbm
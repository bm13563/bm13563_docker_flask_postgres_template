from jwt import decode
from functools import wraps

from flask import request, abort, g, jsonify

from api.config import get_config_value
from api.db import get_dbm
from common.logging import get_logger


logger = get_logger()


class Success():
    def __init__(self, message: str, data: dict) -> None:
        self.code = 200
        self.description = message
        self.data = data

    def to_json(self) -> str:
        return jsonify(self.__dict__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if token is None:
            logger.error("token is missing")
            abort(401, "token is missing")

        try:
            data = decode(token, get_config_value("SECRET_KEY"))
            g.current_user = data.get("user_id")
        except Exception as e:
            logger.error("token is invalid", extra={"error": e})
            abort(401, "token is invalid")

        return f(*args, **kwargs)

    return decorated


def api_error(description):
    def decorator_factory(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                f_return = f(*args, **kwargs)
                return f_return
            except Exception as e:
                if hasattr(e, "code") and hasattr(e, "description"):
                    logger.error("encountered a handled error in resource", extra={"exception": e})
                    abort(e.code, e.description)
                elif hasattr(e, "args") and len(e.args) > 0:
                    logger.error("encountered a handled error in common", extra={"exception": e})
                    abort(500, e.args[0])
                else:
                    logger.error("encountered an unhandled error in resource", extra={"exception": e})
                    abort(500, description)
        
        return decorated

    return decorator_factory



def get_user_by_id(user_id):
    logger.info("getting user by id", extra={"user_id": user_id})
    dbm = get_dbm()
    return dbm.fetch_one(
        """
        select *
        from users
        where user_id = %(user_id)s
    """,
        {"user_id": user_id},
    )


def get_user_by_username(username):
    logger.info("getting user by username", extra={"username": username})
    dbm = get_dbm()
    return dbm.fetch_one(
        """
        select *
        from users
        where username = %(username)s
    """,
        {"username": username},
    )
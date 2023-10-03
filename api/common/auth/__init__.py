from jwt import encode
from uuid import uuid4
from datetime import datetime, timezone

from passlib.hash import sha256_crypt
from flask import abort

from api.db import get_dbm
from api.config import get_config_value
from api.utils import get_user_by_username
from common.logging import get_logger


logger = get_logger()


def generate_token(user_id):
    try:
        valid_for_seconds = get_config_value("JWT_EXPIRATION")
        expiry = datetime.now(tz=timezone.utc).timestamp() + int(valid_for_seconds)
        token = encode(
            {"user_id": user_id, "exp": expiry},
            get_config_value("SECRET_KEY"),
        )
        logger.info("token generated", extra={"user_id": user_id})
        return token
    except Exception as e:
        logger.error("could not generate token", extra={"error": e})
        raise (e)


def password_matches(username, hashed_password):
    user = get_user_by_username(username)

    if not user:
        logger.error("invalid username", extra={"username": username})
        abort(401, "invalid username")
    elif not sha256_crypt.verify(hashed_password, user.get("password") or uuid4()):
        logger.error("invalid password", extra={"username": username})
        abort(401, "invalid password")
    else:
        logger.info("user authenticated", extra={"username": username})
        return user


def register_user(username, password):
    encrypted_password = sha256_crypt.encrypt(password)
    dbm = get_dbm()
    try:
        dbm.execute(
            """
                insert into users (username, password)
                values (%(username)s, %(password)s)
            """,
            {"username": username, "password": encrypted_password},
        )
    except Exception as e:
        logger.error(
            "could not register user", extra={"username": username, "error": e}
        )
        raise (e)


def login_user(username, hashed_password):
    user = password_matches(username, hashed_password)

    if user:
        return generate_token(str(user.get("user_id"))).decode("utf-8")
    else:
        abort(401, "invalid username or password")


def user_can_view_project(user_id, project_id):
    dbm = get_dbm()
    can_view_project = dbm.fetch_one("""
        select *
        from project_users
        where project_id = %(project_id)s
            and user_id = %(user_id)s
    """, {"project_id": project_id, "user_id": user_id})

    return can_view_project is not None
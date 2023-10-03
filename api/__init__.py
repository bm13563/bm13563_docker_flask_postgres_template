from flask import abort

from api.app import create_app
from api.config import get_config
from api.db import get_dbm
from api.utils import Success, token_required, api_error


app = create_app()
with app.app_context():
    get_config()
    get_dbm()


@app.route("/ping", methods=["GET"])
@api_error("Unable to ping")
def ping():
    return Success( "pong", {}).to_json()


@app.route("/protected_ping", methods=["GET"])
@token_required
@api_error("Unable to get ping with authentication")
def protected_ping():
    return Success( "pong", {}).to_json()

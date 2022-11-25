from api.app import create_app
from api.config import get_config
from api.db import get_dbm
from api.resources.auth.auth_common import token_required


app = create_app()
with app.app_context():
    get_config()
    get_dbm()


@app.route("/ping", methods=["GET"])
def ping():
    return {
        "status_code": 200,
        "message": "pong",
        "data": {},
    }


@app.route("/protected_ping", methods=["GET"])
@token_required
def protected_ping():
    return {
        "status_code": 200,
        "message": "protected pong",
        "data": {},
    }

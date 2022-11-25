from api.app import create_app
from api.resources.auth.auth_common import token_required


app = create_app()


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
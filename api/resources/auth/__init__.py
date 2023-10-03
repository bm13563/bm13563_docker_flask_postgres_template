from flask import abort, request, Blueprint

from api.common.auth import register_user, login_user
from api.utils import Success, api_error
from common.logging import get_logger


logger = get_logger()


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
@api_error("Unable to register user")
def register():
    request_data = request.get_json()
    username = request_data.get("username", False)
    password = request_data.get("password", False)

    if not username or not password:
        abort(400, "Username and password are required")

    register_user(username, password)

    return Success("User registered successfully", {}).to_json()


@auth.route("/login", methods=["POST"])
@api_error("Unable to log user in")
def login():
    request_data = request.get_json()
    username = request_data.get("username", False)
    hashed_password = request_data.get("password", False)

    if not username or not hashed_password:
        abort(400, "Username and password are required")

    token = login_user(username, hashed_password)
    
    return Success("User logged in successfully", {"token": token}).to_json()

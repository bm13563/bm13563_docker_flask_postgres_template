from api.common.auth import register_user
from api.app import create_app


def create_test_data():
    """
    This function is used to setup data in the database.
    """
    app = create_app()

    with app.app_context():
        register_user("test_username", "test_password")

    app = None

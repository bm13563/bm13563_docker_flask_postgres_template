from api.resources.auth.auth_controller import register_controller
from api.app import create_app


def setup_data():
    """
        This function is used to setup data in the database.
    """
    app = create_app()

    with app.app_context():
        register_controller("test_username", "test_password")
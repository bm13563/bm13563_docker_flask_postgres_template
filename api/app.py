from flask import Flask

from common.logging import get_logger


logger = get_logger()


def create_app():
    app = Flask(__name__)
    logger.info("starting application")

    from api.resources.auth import auth

    app.register_blueprint(auth)
    logger.info("registered auth blueprint")

    return app

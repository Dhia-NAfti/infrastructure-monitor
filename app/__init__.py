from flask import Flask

from .database import init_db
from .routes import api


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE="infrastructure.db",
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    init_db(app)
    app.register_blueprint(api)
    return app

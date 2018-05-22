from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.basics import basics as basics_blueprint
    app.register_blueprint(basics_blueprint)

    return app

from flask import Flask
import os
from db.dbi.db_interface import DBInterface
import secrets
from flask_login import LoginManager
from config import ProdConfig
from .user import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = secrets.token_hex()

    if test_config is None:
        app.config.from_object("config.ProdConfig")
        db_uri = ProdConfig.POSTGRES_DATABASE_URI
    else:
        app.config.from_object(test_config)
        db_uri = test_config.POSTGRES_DATABASE_URL

    dbi = DBInterface(db_uri)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        poss_user = dbi.get_user_by_id(user_id)

        if poss_user:
            return User(user_id)

        return None

    from . import routes
    app.register_blueprint(routes.bp)

    return app

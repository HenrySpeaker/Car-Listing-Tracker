from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:  # pragma: no cover
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object(test_config)

    from useralerts.api.routes import alerts_bp
    app.register_blueprint(alerts_bp)

    return app

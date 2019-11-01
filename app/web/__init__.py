from flask import Flask
from config import CONFIG


def create_app() -> Flask:
    flask_app: Flask = Flask(__name__)
    flask_app.config.from_object(CONFIG)

    from app.web.controllers.api.client import api_v1_ingredients
    flask_app.register_blueprint(api_v1_ingredients)

    return flask_app


app: Flask = create_app()

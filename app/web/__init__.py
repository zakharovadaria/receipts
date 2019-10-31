from flask import Flask
from config import CONFIG


def create_app() -> Flask:
    flask_app: Flask = Flask(__name__)
    flask_app.config.from_object(CONFIG)

    return flask_app


app: Flask = create_app()

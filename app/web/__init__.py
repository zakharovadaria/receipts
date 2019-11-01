from flask import Flask
from config import CONFIG


def create_app() -> Flask:
    flask_app: Flask = Flask(__name__)
    flask_app.config.from_object(CONFIG)

    from app.web.controllers.api.client.ingredients_controller import api_v1_ingredients
    flask_app.register_blueprint(api_v1_ingredients)

    from app.web.controllers.api.client.receipts_controller import api_v1_receipts
    flask_app.register_blueprint(api_v1_receipts)

    return flask_app


app: Flask = create_app()

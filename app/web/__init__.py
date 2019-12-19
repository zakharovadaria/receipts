from flask import Flask
from config import CONFIG


def create_app() -> Flask:
    flask_app: Flask = Flask(__name__)
    flask_app.config.from_object(CONFIG)

    from app.web.controllers.api.admin import api_admin_v1_bp
    flask_app.register_blueprint(api_admin_v1_bp)

    from app.web.controllers.api.client import api_client_v1_bp
    flask_app.register_blueprint(api_client_v1_bp)

    from app.web.admin_panel import admin_panel
    admin_panel.init_app(flask_app)

    return flask_app


app: Flask = create_app()

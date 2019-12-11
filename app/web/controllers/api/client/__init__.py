from flask import Blueprint
from flask_restplus import Api

from app.web.controllers.api.client.v1.receipts_controller import receipts_namespace

api_client_v1_bp = Blueprint('Clients API', __name__, url_prefix='/api/client/v1')
api_client_v1 = Api(api_client_v1_bp, version='1.0')

api_client_v1.add_namespace(receipts_namespace)

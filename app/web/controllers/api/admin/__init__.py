from flask import Blueprint
from flask_restplus import Api

from app.web.controllers.api.admin.v1.ingredients_controller import ingredients_namespace
from app.web.controllers.api.admin.v1.login_controller import login_namespace
from app.web.controllers.api.admin.v1.receipts_controller import receipts_namespace

api_admin_v1_bp = Blueprint('Admins API', __name__, url_prefix='/api/admin/v1')
api_admin_v1 = Api(api_admin_v1_bp, version='1.0')

api_admin_v1.add_namespace(ingredients_namespace)
api_admin_v1.add_namespace(receipts_namespace)
api_admin_v1.add_namespace(login_namespace)

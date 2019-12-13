from flask_restplus import Resource

from app.web.auth.admin_basic_auth import admin_basic_auth


class AdminResource(Resource):
    method_decorators = [admin_basic_auth.required]

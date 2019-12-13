from flask_restplus import Resource

from app.web.auth.client_basic_auth import client_basic_auth


class ClientResource(Resource):
    method_decorators = [client_basic_auth.required]

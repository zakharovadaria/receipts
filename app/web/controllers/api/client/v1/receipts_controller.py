from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource

from app.models.receipt import Receipt
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts')


@receipts_namespace.route('/', strict_slashes=True)
class ReceiptsListResource(Resource):
    method_decorators = [jwt_required]

    def get(self) -> dict:
        receipts = session.query(Receipt).all()
        receipts = ReceiptClientSchema().dump(receipts, many=True)
        response = BasicResponse(receipts)
        return BasicResponseSchema().dump(response)


@receipts_namespace.route('/<int:id>/', strict_slashes=True)
class ReceiptsResource(Resource):
    method_decorators = [jwt_required]

    def get(self, id: int) -> dict:
        receipt = session.query(Receipt).get(id)
        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)

from flask_restplus import Namespace

from app.models.receipt import Receipt
from app.web.controllers.api.client.client_resource import ClientResource
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts')


@receipts_namespace.route('/', strict_slashes=True)
class ReceiptsListResource(ClientResource):
    def get(self):
        receipts = session.query(Receipt).all()
        receipts = ReceiptClientSchema().dump(receipts, many=True)
        response = BasicResponse(receipts)
        return BasicResponseSchema().dump(response)


@receipts_namespace.route('/<int:id>/', strict_slashes=True)
class ReceiptsResource(ClientResource):
    def get(self, id):
        receipt = session.query(Receipt).get(id)
        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)

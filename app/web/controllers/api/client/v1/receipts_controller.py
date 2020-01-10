from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Namespace, Resource, reqparse

from app.models.receipt import Receipt
from app.models.user import User
from app.web.controllers.entities.basic_error import BasicError
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts')


@receipts_namespace.route('/', strict_slashes=True)
class ReceiptsListResource(Resource):
    method_decorators = [jwt_required]

    def search_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False, default=None)
        args = parser.parse_args()
        return args['user_id']

    def get(self) -> dict:
        user_id = self.search_params()

        if user_id:
            user = session.query(User).get(user_id)
            if not user:
                raise BasicError('User not found.', 404)
            receipts = user.receipts
        else:
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


@receipts_namespace.route('/<int:id>/save/', strict_slashes=True)
class ReceiptsSaveResource(Resource):
    method_decorators = [jwt_required]

    def post(self, id: int) -> dict:
        current_user = get_jwt_identity()
        user = session.query(User).filter(User.email == current_user).one()

        receipt = session.query(Receipt).get(id)

        if not receipt:
            raise BasicError('Receipt not found.', 404)

        user.receipts.append(receipt)

        session.add(user)
        session.commit()

        response = BasicResponse()

        return BasicResponseSchema().dump(response)

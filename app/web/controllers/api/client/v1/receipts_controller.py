from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Namespace, Resource, reqparse, fields

from app.models.receipt import Receipt
from app.models.user import User
from app.web.controllers.entities.basic_error import BasicError
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts')

receipts_fields = receipts_namespace.model('Receipt', {
    'name': fields.String(example='Meat'),
    'description': fields.String(example='Long description'),
    'ingredients': fields.List(fields.Integer(), example=[1]),
    'calories': fields.Float(example=300.0),
    'steps': fields.List(fields.String(), example=['step1, step2']),
})

auth_parser = receipts_namespace.parser()
auth_parser.add_argument('Authorization', location='headers', help='Bearer token')

user_parser = receipts_namespace.parser()
user_parser.add_argument('user_id')


@receipts_namespace.route('/', strict_slashes=True)
@receipts_namespace.expect(auth_parser, validate=True)
class ReceiptsListResource(Resource):
    method_decorators = [jwt_required]

    def search_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False, default=None)
        args = parser.parse_args()
        return args['user_id']

    @receipts_namespace.doc(model=receipts_fields)
    @receipts_namespace.expect(user_parser, validate=True)
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
@receipts_namespace.expect(auth_parser, validate=True)
@receipts_namespace.doc(params={'id': 'Receipt ID'})
class ReceiptsResource(Resource):
    method_decorators = [jwt_required]

    @receipts_namespace.doc(model=receipts_fields)
    def get(self, id: int) -> dict:
        receipt = session.query(Receipt).get(id)
        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)


@receipts_namespace.route('/<int:id>/save/', strict_slashes=True)
@receipts_namespace.expect(auth_parser, validate=True)
@receipts_namespace.doc(params={'id': 'Receipt ID'})
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

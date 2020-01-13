from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, reqparse, Resource, fields

from app.models.ingredient import Ingredient
from app.models.receipt import Receipt
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts CRUD')

receipts_fields = receipts_namespace.model('Receipt', {
    'name': fields.String(example='Meat'),
    'description': fields.String(example='Long description'),
    'ingredients': fields.List(fields.Integer(), example=[1]),
    'calories': fields.Float(example=300.0),
    'steps': fields.List(fields.String(), example=['step1, step2']),
})

auth_parser = receipts_namespace.parser()
auth_parser.add_argument('Authorization', location='headers', help='Bearer token')


@receipts_namespace.route('/', strict_slashes=True)
@receipts_namespace.expect(auth_parser, validate=True)
class ReceiptsListResource(Resource):
    method_decorators = [jwt_required]

    def create_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=False, default='')
        parser.add_argument('ingredients', type=int, action='append', required=False, default=None)
        parser.add_argument('calories', type=float, required=False, default=0)
        parser.add_argument('steps', type=str, action='append', required=False, default=None)
        return parser.parse_args()

    def get(self) -> dict:
        receipts = session.query(Receipt).all()
        receipts = ReceiptClientSchema().dump(receipts, many=True)
        response = BasicResponse(receipts)
        return BasicResponseSchema().dump(response)

    @receipts_namespace.doc(model=receipts_fields)
    @receipts_namespace.expect(receipts_fields, validate=True)
    def post(self) -> dict:
        create_params = self.create_params()
        create_params["ingredients"] = session.query(Ingredient).filter(Ingredient.id.in_(create_params["ingredients"])).all()
        receipt = Receipt(**create_params)

        session.add(receipt)
        session.commit()

        receipt = session.query(Receipt).one()

        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)


@receipts_namespace.route('/<int:id>/', strict_slashes=True)
@receipts_namespace.doc(params={'id': 'Receipt ID'})
@receipts_namespace.expect(auth_parser, validate=True)
class ReceiptsResource(Resource):
    method_decorators = [jwt_required]

    def update_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, store_missing=False, required=False)
        parser.add_argument('description', type=str, store_missing=False, required=False)
        parser.add_argument('ingredients', type=int, store_missing=False, action='append', required=False)
        parser.add_argument('calories', type=float, store_missing=False, required=False)
        parser.add_argument('steps', type=str, store_missing=False, action='append', required=False)
        return parser.parse_args()

    @receipts_namespace.doc(model=receipts_fields)
    def get(self, id: int) -> dict:
        receipt = session.query(Receipt).get(id)
        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)

    @receipts_namespace.doc(model=receipts_fields)
    @receipts_namespace.expect(receipts_fields, validate=True)
    def put(self, id: int) -> dict:
        receipt = session.query(Receipt).get(id)

        update_params = self.update_params()
        if 'ingredients' in update_params:
            update_params['ingredients'] = session.query(Ingredient).filter(Ingredient.id.in_(update_params["ingredients"])).all()

        for key, value in update_params.items():
            setattr(receipt, key, value)

        session.commit()

        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)

    def delete(self, id: int) -> dict:
        receipt = session.query(Receipt).get(id)
        session.delete(receipt)
        session.commit()
        response = BasicResponse(None)
        return BasicResponseSchema().dump(response)

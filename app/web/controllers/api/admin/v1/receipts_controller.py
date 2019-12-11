from flask_restplus import Namespace, reqparse, Resource

from app.models.ingredient import Ingredient
from app.models.receipt import Receipt
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import ReceiptClientSchema

receipts_namespace = Namespace('receipts', description='Receipts CRUD')


@receipts_namespace.route('/', strict_slashes=True)
class ReceiptsListResource(Resource):
    def create_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=False, default='')
        parser.add_argument('ingredients', type=int, action='append', required=False, default=None)
        parser.add_argument('calories', type=float, required=False, default=0)
        parser.add_argument('steps', type=str, action='append', required=False, default=None)
        return parser.parse_args()

    def get(self):
        receipts = session.query(Receipt).all()
        receipts = ReceiptClientSchema().dump(receipts, many=True)
        response = BasicResponse(receipts)
        return BasicResponseSchema().dump(response)

    def post(self):
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
class ReceiptsResource(Resource):
    def update_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, store_missing=False, required=False)
        parser.add_argument('description', type=str, store_missing=False, required=False)
        parser.add_argument('ingredients', type=int, store_missing=False, action='append', required=False)
        parser.add_argument('calories', type=float, store_missing=False, required=False)
        parser.add_argument('steps', type=str, store_missing=False, action='append', required=False)
        return parser.parse_args()

    def get(self, id):
        receipt = session.query(Receipt).get(id)
        receipt = ReceiptClientSchema().dump(receipt)
        response = BasicResponse(receipt)
        return BasicResponseSchema().dump(response)

    def put(self, id):
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

    def delete(self, id):
        receipt = session.query(Receipt).get(id)
        session.delete(receipt)
        session.commit()
        response = BasicResponse(None)
        return BasicResponseSchema().dump(response)

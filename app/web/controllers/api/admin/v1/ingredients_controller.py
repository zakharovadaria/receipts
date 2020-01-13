from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, reqparse, Resource, fields

from app.models.ingredient import Ingredient
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import IngredientClientSchema

ingredients_namespace = Namespace('ingredients', description='Ingredients CRUD')

ingredients_fields = ingredients_namespace.model('Ingredient', {
    'name': fields.String(example='Egg'),
    'calories': fields.Float(example=200.0),
})

auth_parser = ingredients_namespace.parser()
auth_parser.add_argument('Authorization', location='headers', help='Bearer token')


@ingredients_namespace.route('/', strict_slashes=True)
@ingredients_namespace.expect(auth_parser, validate=True)
class IngredientsListResource(Resource):
    method_decorators = [jwt_required]

    def create_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('calories', type=float, required=True)
        return parser.parse_args()

    def get(self) -> dict:
        ingredients = session.query(Ingredient).all()
        ingredients = IngredientClientSchema().dump(ingredients, many=True)
        response = BasicResponse(ingredients)
        return BasicResponseSchema().dump(response)

    @ingredients_namespace.doc(model=ingredients_fields)
    @ingredients_namespace.expect(ingredients_fields, validate=True)
    def post(self) -> dict:
        create_params = self.create_params()
        ingredient = Ingredient(**create_params)

        session.add(ingredient)
        session.commit()

        ingredient = IngredientClientSchema().dump(ingredient)
        response = BasicResponse(ingredient)
        return BasicResponseSchema().dump(response)


@ingredients_namespace.route('/<int:id>/', strict_slashes=True)
@ingredients_namespace.doc(params={'id': 'Ingredient ID'})
@ingredients_namespace.expect(auth_parser, validate=True)
class IngredientsResource(Resource):
    method_decorators = [jwt_required]

    def update_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, store_missing=False, required=False)
        parser.add_argument('calories', type=float, store_missing=False, required=False)
        return parser.parse_args()

    @ingredients_namespace.doc(model=ingredients_fields)
    def get(self, id: int) -> dict:
        ingredient = session.query(Ingredient).get(id)
        ingredient = IngredientClientSchema().dump(ingredient)
        response = BasicResponse(ingredient)
        return BasicResponseSchema().dump(response)

    @ingredients_namespace.doc(model=ingredients_fields)
    @ingredients_namespace.expect(ingredients_fields, validate=True)
    def put(self, id: int) -> dict:
        ingredient = session.query(Ingredient).get(id)

        update_params = self.update_params()

        for key, value in update_params.items():
            setattr(ingredient, key, value)

        session.commit()

        ingredient = IngredientClientSchema().dump(ingredient)
        response = BasicResponse(ingredient)
        return BasicResponseSchema().dump(response)

    def delete(self, id: int) -> dict:
        ingredient = session.query(Ingredient).get(id)
        session.delete(ingredient)
        session.commit()

        response = BasicResponse(None)
        return BasicResponseSchema().dump(response)

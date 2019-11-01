from flask import Blueprint, request

from app.models.ingredient import Ingredient
from db import session
from schemas import IngredientClientSchema

api_v1_ingredients = Blueprint('ingredients', __name__, url_prefix='/api/v1/ingredients')


@api_v1_ingredients.route('/', methods=['GET'], strict_slashes=True)
def index():
    ingredients = session.query(Ingredient).all()
    ingredients = IngredientClientSchema().dump(ingredients, many=True)
    return ({
        "result": ingredients,
    })


@api_v1_ingredients.route('/<int:id>', methods=['GET'], strict_slashes=True)
def show(id):
    ingredient = session.query(Ingredient).get(id)
    ingredient = IngredientClientSchema().dump(ingredient)
    return ({
        "result": ingredient,
    })


@api_v1_ingredients.route('/', methods=['POST'], strict_slashes=True)
def create():
    response = request.get_json(force=True)
    ingredient = Ingredient(name=response["name"], calories=response["calories"])

    session.add(ingredient)
    session.commit()

    ingredient = session.query(Ingredient).one()

    ingredient = IngredientClientSchema().dump(ingredient)
    return ({
        "result": ingredient,
    })


@api_v1_ingredients.route('/<int:id>', methods=['PUT'], strict_slashes=True)
def update(id):
    ingredient = session.query(Ingredient).get(id)

    params = request.get_json(force=True)

    if 'name' in params:
        ingredient.name = params['name']

    if 'calories' in params:
        ingredient.calories = params['calories']

    session.commit()

    ingredient = IngredientClientSchema().dump(ingredient)
    return ({
        "result": ingredient,
    })


@api_v1_ingredients.route('/<int:id>', methods=['DELETE'], strict_slashes=True)
def delete(id):
    ingredient = session.query(Ingredient).get(id)
    session.delete(ingredient)
    session.commit()

    return ({
        "result": None,
    })

from flask import Blueprint, request

from app.models.ingredient import Ingredient
from app.models.receipt import Receipt
from db import session
from schemas import ReceiptClientSchema

api_v1_receipts = Blueprint('receipts', __name__, url_prefix='/api/v1/receipts')


@api_v1_receipts.route('/', methods=['GET'], strict_slashes=True)
def index():
    receipts = session.query(Receipt).all()
    receipts = ReceiptClientSchema().dump(receipts, many=True)
    return ({
        "result": receipts,
    })


@api_v1_receipts.route('/<int:id>', methods=['GET'], strict_slashes=True)
def show(id):
    ingredient = session.query(Receipt).get(id)
    ingredient = ReceiptClientSchema().dump(ingredient)
    return ({
        "result": ingredient,
    })


@api_v1_receipts.route('/', methods=['POST'], strict_slashes=True)
def create():
    response = request.get_json(force=True)
    ingredients = session.query(Ingredient).filter(Ingredient.id.in_(response["ingredients"])).all()
    receipt = Receipt(
        name=response["name"],
        description=response["description"],
        calories=response["calories"],
        ingredients=ingredients,
        steps=response["steps"]
    )

    session.add(receipt)
    session.commit()

    ingredient = session.query(Receipt).one()

    ingredient = ReceiptClientSchema().dump(ingredient)
    return ({
        "result": ingredient,
    })


@api_v1_receipts.route('/<int:id>', methods=['PUT'], strict_slashes=True)
def update(id):
    receipt = session.query(Receipt).get(id)

    params = request.get_json(force=True)

    if 'name' in params:
        receipt.name = params['name']

    if 'description' in params:
        receipt.description = params['description']

    if 'calories' in params:
        receipt.calories = params['calories']

    if 'ingredients' in params:
        ingredients = session.query(Ingredient).filter(Ingredient.id.in_(params["ingredients"])).all()
        receipt.ingredients = ingredients

    if 'steps' in params:
        receipt.steps = params['steps']

    session.commit()

    receipt = ReceiptClientSchema().dump(receipt)
    return ({
        "result": receipt,
    })


@api_v1_receipts.route('/<int:id>', methods=['DELETE'], strict_slashes=True)
def delete(id):
    receipt = session.query(Receipt).get(id)
    session.delete(receipt)
    session.commit()

    return ({
        "result": None,
    })
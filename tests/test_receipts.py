from app.models.ingredient import Ingredient
from db import session
from app.models.receipt import Receipt


def prepare_create_receipt():
    first_ingredient = Ingredient(name='Name', calories=200)
    session.add(first_ingredient)

    second_ingredient = Ingredient(name='Name1', calories=201)
    session.add(second_ingredient)

    session.commit()

    first_step = 'First step'
    second_step = 'Second step'

    return first_ingredient, second_ingredient, first_step, second_step


def test_create_receipt():
    first_ingredient, second_ingredient, first_step, second_step = prepare_create_receipt()

    receipt = Receipt(
        name='Name',
        description='Cool',
        calories=200,
        ingredients=[first_ingredient, second_ingredient],
        steps=[first_step, second_step],
    )

    session.add(receipt)
    session.commit()

    actual = session.query(Receipt).count()
    expected = 1

    assert actual == expected


def test_created_receipt():
    first_ingredient, second_ingredient, first_step, second_step = prepare_create_receipt()

    receipt = Receipt(
        name='Name',
        description='Cool',
        calories=200,
        ingredients=[first_ingredient, second_ingredient],
        steps=[first_step, second_step],
    )

    session.add(receipt)
    session.commit()

    actual = session.query(Receipt).one()
    expected = receipt

    assert actual == expected

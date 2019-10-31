from db import session
from app.models.ingredient import Ingredient


def test_create_ingredients():
    ingredient = Ingredient(name='Name', calories=120)
    session.add(ingredient)
    session.commit()

    actual = session.query(Ingredient).count()
    expected = 1

    assert actual == expected


def test_created_ingredients():
    ingredient = Ingredient(name='Name', calories=120)
    session.add(ingredient)
    session.commit()

    actual = session.query(Ingredient).one()
    expected = ingredient

    assert actual == expected

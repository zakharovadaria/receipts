import pytest

from app.models.ingredient import Ingredient
from app.models.ingredients_receipts import IngredientsReceipts
from app.models.receipt import Receipt

from app.web import create_app


@pytest.fixture(scope="function", autouse=True)
def execute_before_any_test():
    IngredientsReceipts.truncate()
    Receipt.truncate()
    Ingredient.truncate()


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def test_client(app):
    return app.test_client()

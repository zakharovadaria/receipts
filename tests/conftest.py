import base64

import pytest

from app.models.ingredient import Ingredient
from app.models.ingredients_receipts import IngredientsReceipts
from app.models.receipt import Receipt

from app.web import create_app
from config import CONFIG


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


def get_key(username: str, password: str):
    token = f'{username}:{password}'.encode()
    token = base64.b64encode(token).decode()
    return token


@pytest.fixture()
def admin_key():
    username = CONFIG.BASIC_AUTH_ADMIN_NAME
    password = CONFIG.BASIC_AUTH_ADMIN_PASS
    return get_key(username, password)


@pytest.fixture()
def client_key():
    username = CONFIG.BASIC_AUTH_CLIENT_NAME
    password = CONFIG.BASIC_AUTH_CLIENT_PASS
    return get_key(username, password)

import base64

import pytest

from app.models.ingredient import Ingredient
from app.models.ingredients_receipts import IngredientsReceipts
from app.models.receipt import Receipt
from app.models.user import User

from app.web import create_app
from app.web.bcrypt import bcrypt
from config import CONFIG
from db import session


@pytest.fixture(scope="function", autouse=True)
def execute_before_any_test():
    IngredientsReceipts.truncate()
    Receipt.truncate()
    Ingredient.truncate()
    User.truncate()


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def test_client(app):
    return app.test_client()


def get_password() -> str:
    return 'pass'


@pytest.fixture()
def user_password() -> str:
    return get_password()


def create_user(role: str) -> User:
    email = f'{role}@test.com'
    password = get_password()

    hash_password = bcrypt.generate_password_hash(password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email=email,
        password=hash_password,
        role=role
    )

    session.add(user)
    session.commit()

    return user


def get_headers(access_token: str, token_type: str) -> dict:
    return {'Authorization': f'{token_type} {access_token}'}


@pytest.fixture()
def client():
    user = create_user('client')

    return user


@pytest.fixture()
def admin():
    user = create_user('admin')

    return user


@pytest.fixture()
def admin_headers(test_client, admin):
    data = {
        "email": admin.email,
        "password": get_password()
    }

    response = test_client.post('/api/admin/v1/login/', json=data)
    result = response.json['result']

    access_token = result['access_token']

    return get_headers(access_token, 'Bearer')


@pytest.fixture()
def client_headers(test_client, client):
    data = {
        "email": client.email,
        "password": get_password()
    }

    response = test_client.post('/api/client/v1/login/', json=data)
    result = response.json['result']

    access_token = result['access_token']

    return get_headers(access_token, 'Bearer')


@pytest.fixture()
def admin_panel_headers():
    username = CONFIG.BASIC_AUTH_ADMIN_PANEL_NAME
    password = CONFIG.BASIC_AUTH_ADMIN_PANEL_PASS
    token = f'{username}:{password}'.encode()
    token = base64.b64encode(token).decode()
    return get_headers(token, 'Basic')

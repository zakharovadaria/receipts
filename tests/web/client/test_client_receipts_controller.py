from flask.testing import FlaskClient

from app.models.receipt import Receipt
from db import session
from schemas import ReceiptClientSchema
from tests.test_receipts import prepare_create_receipt


def test_status_without_auth(test_client: FlaskClient):
    response = test_client.get('/api/client/v1/receipts/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client: FlaskClient, client_headers: dict):
    response = test_client.get('/api/client/v1/receipts/', headers=client_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_count(test_client: FlaskClient, client_headers: dict):
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

    response = test_client.get('/api/client/v1/receipts/', headers=client_headers)
    actual = len(response.json['result'])
    expected = 1

    assert actual == expected


def test_get(test_client: FlaskClient, client_headers: dict):
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

    response = test_client.get('/api/client/v1/receipts/', headers=client_headers)
    actual = response.json['result'][0]
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_show(test_client: FlaskClient, client_headers: dict):
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

    response = test_client.get(f"/api/client/v1/receipts/{receipt.id}/", headers=client_headers)
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected

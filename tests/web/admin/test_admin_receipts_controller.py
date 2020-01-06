from flask.testing import FlaskClient

from app.models.receipt import Receipt
from db import session
from schemas import ReceiptClientSchema
from tests.test_receipts import prepare_create_receipt


def test_status_without_auth(test_client: FlaskClient):
    response = test_client.get('/api/admin/v1/receipts/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client: FlaskClient, admin_headers: dict):
    response = test_client.get('/api/admin/v1/receipts/', headers=admin_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_count(test_client: FlaskClient, admin_headers: dict):
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

    response = test_client.get('/api/admin/v1/receipts/', headers=admin_headers)
    actual = len(response.json['result'])
    expected = 1

    assert actual == expected


def test_get(test_client: FlaskClient, admin_headers: dict):
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

    response = test_client.get('/api/admin/v1/receipts/', headers=admin_headers)
    actual = response.json['result'][0]
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_show(test_client: FlaskClient, admin_headers: dict):
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

    response = test_client.get(f"/api/admin/v1/receipts/{receipt.id}/", headers=admin_headers)
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_create(test_client: FlaskClient, admin_headers: dict):
    first_ingredient, second_ingredient, first_step, second_step = prepare_create_receipt()

    data = ({
        "name": 'Name',
        "description": 'Cool',
        "calories": 200,
        "ingredients": [first_ingredient.id, second_ingredient.id],
        "steps": [first_step, second_step],
    })

    response = test_client.post('/api/admin/v1/receipts/', json=data, headers=admin_headers)
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(session.query(Receipt).one())

    assert actual == expected


def test_update(test_client: FlaskClient, admin_headers: dict):
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

    data = ({
        "name": 'Name1',
        "description": 'Cool1',
        "calories": 201,
        "ingredients": [second_ingredient.id],
        "steps": [first_step],
    })

    response = test_client.put(f"/api/admin/v1/receipts/{receipt.id}/", json=data, headers=admin_headers)
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_delete(test_client: FlaskClient, admin_headers: dict):
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

    test_client.delete(f"/api/admin/v1/receipts/{receipt.id}/", headers=admin_headers)
    actual = session.query(Receipt).count()
    expected = 0

    assert actual == expected

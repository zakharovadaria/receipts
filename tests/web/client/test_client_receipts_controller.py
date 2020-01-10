from flask.testing import FlaskClient

from app.models.receipt import Receipt
from app.models.user import User
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


def test_save_receipt(test_client: FlaskClient, client_headers: dict):
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

    response = test_client.post(f'/api/client/v1/receipts/{receipt.id}/save/', headers=client_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_save_receipt_with_error_receipt_id(test_client: FlaskClient, client_headers: dict):
    response = test_client.post(f'/api/client/v1/receipts/1/save/', headers=client_headers)
    actual = response.status_code
    expected = 404

    assert actual == expected


def test_get_saved_receipts(test_client: FlaskClient, client_headers: dict, client: User):
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

    test_client.post(f'/api/client/v1/receipts/{receipt.id}/save/', headers=client_headers)

    response = test_client.get(f'/api/client/v1/receipts/?user_id={client.id}', headers=client_headers)

    result = response.json['result']

    actual = len(result)
    expected = 1

    assert actual == expected

    actual = result[0]
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_get_saved_receipts_with_error_user_id(test_client: FlaskClient, client_headers: dict, client: User):
    response = test_client.get(f'/api/client/v1/receipts/?user_id={client.id * 10}', headers=client_headers)

    actual = response.status_code
    expected = 404

    assert actual == expected

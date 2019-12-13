from app.models.receipt import Receipt
from db import session
from schemas import ReceiptClientSchema
from tests.test_receipts import prepare_create_receipt


def test_status_without_auth(test_client):
    response = test_client.get('/api/admin/v1/receipts/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client, admin_key):
    response = test_client.get('/api/admin/v1/receipts/', headers={'Authorization': f'Basic {admin_key}'})
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_count(test_client, admin_key):
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

    response = test_client.get('/api/admin/v1/receipts/', headers={'Authorization': f'Basic {admin_key}'})
    actual = len(response.json['result'])
    expected = 1

    assert actual == expected


def test_get(test_client, admin_key):
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

    response = test_client.get('/api/admin/v1/receipts/', headers={'Authorization': f'Basic {admin_key}'})
    actual = response.json['result'][0]
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_show(test_client, admin_key):
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

    response = test_client.get(f"/api/admin/v1/receipts/{receipt.id}/", headers={'Authorization': f'Basic {admin_key}'})
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_create(test_client, admin_key):
    first_ingredient, second_ingredient, first_step, second_step = prepare_create_receipt()

    data = ({
        "name": 'Name',
        "description": 'Cool',
        "calories": 200,
        "ingredients": [first_ingredient.id, second_ingredient.id],
        "steps": [first_step, second_step],
    })

    response = test_client.post('/api/admin/v1/receipts/', json=data, headers={'Authorization': f'Basic {admin_key}'})
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(session.query(Receipt).one())

    assert actual == expected


def test_update(test_client, admin_key):
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

    response = test_client.put(f"/api/admin/v1/receipts/{receipt.id}/", json=data, headers={'Authorization': f'Basic {admin_key}'})
    actual = response.json['result']
    expected = ReceiptClientSchema().dump(receipt)

    assert actual == expected


def test_delete(test_client, admin_key):
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

    test_client.delete(f"/api/admin/v1/receipts/{receipt.id}/", headers={'Authorization': f'Basic {admin_key}'})
    actual = session.query(Receipt).count()
    expected = 0

    assert actual == expected

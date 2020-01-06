from app.models.ingredient import Ingredient
from db import session
from schemas import IngredientClientSchema


def test_status_without_auth(test_client):
    response = test_client.get('/api/admin/v1/ingredients/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client, admin_headers):
    response = test_client.get('/api/admin/v1/ingredients/', headers=admin_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_count(test_client, admin_headers):
    ingredient = Ingredient(name='Name', calories=200)
    session.add(ingredient)
    session.commit()

    response = test_client.get('/api/admin/v1/ingredients/', headers=admin_headers)
    actual = len(response.json['result'])
    expected = 1

    assert actual == expected


def test_get(test_client, admin_headers):
    ingredient = Ingredient(name='Name', calories=200)
    session.add(ingredient)
    session.commit()

    response = test_client.get('/api/admin/v1/ingredients/', headers=admin_headers)
    actual = response.json['result'][0]
    expected = IngredientClientSchema().dump(ingredient)

    assert actual == expected


def test_show(test_client, admin_headers):
    ingredient = Ingredient(name='Name', calories=200)
    session.add(ingredient)
    session.commit()

    response = test_client.get(f"/api/admin/v1/ingredients/{ingredient.id}/", headers=admin_headers)
    actual = response.json['result']
    expected = IngredientClientSchema().dump(ingredient)

    assert actual == expected


def test_create(test_client, admin_headers):
    data = ({
        "name": "Name",
        "calories": 200,
    })
    response = test_client.post('/api/admin/v1/ingredients/', json=data, headers=admin_headers)

    actual = response.json['result']
    expected = IngredientClientSchema().dump(session.query(Ingredient).one())

    assert actual == expected


def test_update(test_client, admin_headers):
    ingredient = Ingredient(name='Name', calories=200)
    session.add(ingredient)
    session.commit()

    data = ({
        "name": "Name111",
        "calories": 2001,
    })
    response = test_client.put(f"/api/admin/v1/ingredients/{ingredient.id}/", json=data, headers=admin_headers)

    actual = response.json['result']
    expected = IngredientClientSchema().dump(ingredient)

    assert actual == expected


def test_delete(test_client, admin_headers):
    ingredient = Ingredient(name='Name', calories=200)
    session.add(ingredient)
    session.commit()

    test_client.delete(f"/api/admin/v1/ingredients/{ingredient.id}/", headers=admin_headers)
    actual = session.query(Ingredient).count()
    expected = 0

    assert actual == expected

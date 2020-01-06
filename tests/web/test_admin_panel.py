from flask.testing import FlaskClient


def test_status_without_auth(test_client: FlaskClient):
    response = test_client.get('/admin/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client: FlaskClient, admin_panel_headers: dict):
    response = test_client.get('/admin/', headers=admin_panel_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_ingredients_status(test_client: FlaskClient, admin_panel_headers: dict):
    response = test_client.get('/admin/ingredients/', headers=admin_panel_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_receipts_status(test_client: FlaskClient, admin_panel_headers: dict):
    response = test_client.get('/admin/receipts/', headers=admin_panel_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected

def test_status_without_auth(test_client):
    response = test_client.get('/admin/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client, admin_key):
    response = test_client.get('/admin/', headers={'Authorization': f'Basic {admin_key}'})
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_ingredients_status(test_client, admin_key):
    response = test_client.get('/admin/ingredients/', headers={'Authorization': f'Basic {admin_key}'})
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_receipts_status(test_client, admin_key):
    response = test_client.get('/admin/receipts/', headers={'Authorization': f'Basic {admin_key}'})
    actual = response.status_code
    expected = 200

    assert actual == expected

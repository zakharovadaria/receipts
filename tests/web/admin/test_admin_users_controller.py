from flask.testing import FlaskClient

from app.models.user import User
from app.web.bcrypt import bcrypt
from db import session
from schemas import UserClientSchema


def test_status_without_auth(test_client: FlaskClient):
    response = test_client.get('/api/admin/v1/users/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_status(test_client: FlaskClient, admin_headers: dict):
    response = test_client.get('/api/admin/v1/users/', headers=admin_headers)
    actual = response.status_code
    expected = 200

    assert actual == expected


def test_get(test_client: FlaskClient, admin_headers: dict, admin: User):
    response = test_client.get('/api/admin/v1/users/', headers=admin_headers)
    actual = response.json['result'][0]
    expected = UserClientSchema().dump(admin)

    assert actual == expected


def test_show(test_client: FlaskClient, admin_headers: dict, admin: User):
    response = test_client.get(f"/api/admin/v1/users/{admin.id}/", headers=admin_headers)
    actual = response.json['result']
    expected = UserClientSchema().dump(admin)

    assert actual == expected


def test_create_with_used_email(test_client: FlaskClient, admin_headers: dict, admin: User, user_password: str):
    data = ({
        "email": admin.email,
        "password": user_password,
        "role": admin.role,
    })

    response = test_client.post('/api/admin/v1/users/', json=data, headers=admin_headers)
    actual = response.status_code
    expected = 400

    assert actual == expected


def test_create(test_client: FlaskClient, admin_headers: dict, user_password: str):
    data = ({
        "email": 'user@test.com',
        "password": user_password,
        "role": 'admin',
        "active": True,
    })

    response = test_client.post('/api/admin/v1/users/', json=data, headers=admin_headers)
    actual = response.json['result']

    user = session.query(User).filter(User.email == data["email"]).one()
    expected = UserClientSchema().dump(user)

    assert actual == expected


def test_update(test_client: FlaskClient, admin_headers: dict, user_password: str):
    hash_password = bcrypt.generate_password_hash(user_password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email='user@test.com',
        password=hash_password,
        role='admin',
        active=True,
    )

    session.add(user)
    session.commit()

    data = ({
        "email": 'user1@test.com',
        "password": f'{user_password}1',
        "role": 'client',
    })

    response = test_client.put(f"/api/admin/v1/users/{user.id}/", json=data, headers=admin_headers)
    actual = response.json['result']
    expected = UserClientSchema().dump(user)

    assert actual == expected


def test_deactivate_admin(test_client: FlaskClient, admin_headers: dict, user_password: str):
    hash_password = bcrypt.generate_password_hash(user_password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email='user@test.com',
        password=hash_password,
        role='admin',
    )

    session.add(user)
    session.commit()

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data)

    actual = response.status_code
    expected = 200

    assert actual == expected

    data = {
        "active": False,
    }

    test_client.put(f"/api/admin/v1/users/{user.id}/", json=data, headers=admin_headers)

    actual = user.active
    expected = False

    assert actual == expected

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data)

    actual = response.status_code
    expected = 400

    assert actual == expected


def test_activate_admin(test_client: FlaskClient, admin_headers: dict, user_password: str):
    hash_password = bcrypt.generate_password_hash(user_password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email='user@test.com',
        password=hash_password,
        role='admin',
        active=False,
    )

    session.add(user)
    session.commit()

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data)

    actual = response.status_code
    expected = 400

    assert actual == expected

    data = {
        "active": True,
    }

    test_client.put(f"/api/admin/v1/users/{user.id}/", json=data, headers=admin_headers)

    actual = user.active
    expected = True

    assert actual == expected

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data)

    actual = response.status_code
    expected = 200

    assert actual == expected


def test_deactivate_client(test_client: FlaskClient, admin_headers: dict, user_password: str):
    hash_password = bcrypt.generate_password_hash(user_password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email='user@test.com',
        password=hash_password,
        role='client',
    )

    session.add(user)
    session.commit()

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/client/v1/login/', json=data)

    actual = response.status_code
    expected = 200

    assert actual == expected

    data = {
        "active": False,
    }

    test_client.put(f"/api/admin/v1/users/{user.id}/", json=data, headers=admin_headers)

    actual = user.active
    expected = False

    assert actual == expected

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/client/v1/login/', json=data)

    actual = response.status_code
    expected = 400

    assert actual == expected


def test_activate_client(test_client: FlaskClient, admin_headers: dict, user_password: str):
    hash_password = bcrypt.generate_password_hash(user_password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email='user@test.com',
        password=hash_password,
        role='client',
        active=False,
    )

    session.add(user)
    session.commit()

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/client/v1/login/', json=data)

    actual = response.status_code
    expected = 400

    assert actual == expected

    data = {
        "active": True,
    }

    test_client.put(f"/api/admin/v1/users/{user.id}/", json=data, headers=admin_headers)

    actual = user.active
    expected = True

    assert actual == expected

    data = {
        "email": user.email,
        "password": user_password,
    }

    response = test_client.post('/api/client/v1/login/', json=data)

    actual = response.status_code
    expected = 200

    assert actual == expected

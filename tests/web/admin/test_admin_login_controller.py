from app.models.user import User
from app.web.bcrypt import bcrypt
from db import session


def test_status_without_auth(test_client):
    response = test_client.post('/api/admin/v1/login/')
    actual = response.status_code
    expected = 401

    assert actual == expected


def test_login(test_client, admin_key):
    email = 'test@test.com'
    password = 'pass'

    hash_password = bcrypt.generate_password_hash(password)
    hash_password = hash_password.decode('utf-8')

    user = User(
        email=email,
        password=hash_password,
        role='admin'
    )

    session.add(user)
    session.commit()

    data = {
        "email": email,
        "password": password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data, headers={'Authorization': f'Basic {admin_key}'})

    actual = response.status_code
    expected = 200

    assert actual == expected

    actual = response.json['result']

    assert actual['access_token']
    assert actual['refresh_token']

    user = session.query(User).filter(User.email == email).first()

    assert user.authenticated

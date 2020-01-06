from flask.testing import FlaskClient

from app.models.user import User
from db import session


def test_login(test_client: FlaskClient, admin: User, user_password: str):
    data = {
        "email": admin.email,
        "password": user_password,
    }

    response = test_client.post('/api/admin/v1/login/', json=data)

    actual = response.status_code
    expected = 200

    assert actual == expected

    actual = response.json['result']

    assert actual['access_token']
    assert actual['refresh_token']

    user = session.query(User).filter(User.email == admin.email).first()

    assert user.authenticated

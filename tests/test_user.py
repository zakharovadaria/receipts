from db import session
from app.models.user import User


def test_create_user():
    user = User(
        email='test@test.com',
        password='pass'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).count()
    expected = 1

    assert actual == expected


def test_created_user():
    user = User(
        email='test@test.com',
        password='pass'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).one()
    expected = user

    assert actual == expected


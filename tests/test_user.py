from db import session
from app.models.user import User


def test_create_client():
    user = User(
        email='test@test.com',
        password='pass',
        role='client'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).count()
    expected = 1

    assert actual == expected


def test_created_client():
    user = User(
        email='test@test.com',
        password='pass',
        role='client'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).one()
    expected = user

    assert actual == expected


def test_create_admin():
    user = User(
        email='test@test.com',
        password='pass',
        role='admin'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).count()
    expected = 1

    assert actual == expected


def test_created_admin():
    user = User(
        email='test@test.com',
        password='pass',
        role='admin'
    )

    session.add(user)
    session.commit()

    actual = session.query(User).one()
    expected = user

    assert actual == expected

from sqlalchemy import Column, Integer, String, Boolean

from db import Base, session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, primary_key=True, unique=True)
    password = Column(String, nullable=False)
    authenticated = Column(Boolean, default=False)
    role = Column(String, nullable=False)

    @classmethod
    def truncate(cls):
        session.query(User).delete()

    def __str__(self):
        return f'{self.email}'
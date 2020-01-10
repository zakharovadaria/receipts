from sqlalchemy import Column, Integer, ForeignKey

from db import Base, session


class UsersReceipts(Base):
    __tablename__ = 'users_receipts'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'), primary_key=True)

    @classmethod
    def truncate(cls):
        session.query(UsersReceipts).delete()

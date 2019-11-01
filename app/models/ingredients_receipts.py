from sqlalchemy import Column, Integer, String, ForeignKey

from db import Base, session


class IngredientsReceipts(Base):
    __tablename__ = 'ingredients_receipts'
    receipt_id = Column(Integer, ForeignKey('receipts.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    extra_data = Column(String(50))

    @classmethod
    def truncate(cls):
        session.query(IngredientsReceipts).delete()

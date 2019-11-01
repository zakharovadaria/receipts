from sqlalchemy import Column, Integer, String, Float, Text, ARRAY
from sqlalchemy.orm import relationship

from db import Base, session

from app.models.ingredient import Ingredient
from app.models.ingredients_receipts import IngredientsReceipts


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    calories = Column(Float)
    ingredients = relationship("Ingredient", secondary='ingredients_receipts')
    steps = Column(ARRAY(String), nullable=False, default=[], server_default='{}')

    @classmethod
    def truncate(cls):
        session.query(Receipt).delete()

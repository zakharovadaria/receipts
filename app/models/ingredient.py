from sqlalchemy import Column, Integer, String, Float
from db import Base


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Float)

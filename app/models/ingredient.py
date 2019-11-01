from sqlalchemy import Column, Integer, String, Float

from db import Base, session


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Float)

    @classmethod
    def truncate(cls):
        session.query(Ingredient).delete()

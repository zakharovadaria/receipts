from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import CONFIG

engine = create_engine(CONFIG.DATABASE_URL)

Base = declarative_base()
Base.metadata.bind(engine)

Session = sessionmaker(bind=engine)
session = Session()

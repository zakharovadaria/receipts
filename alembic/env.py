from logging.config import fileConfig

from alembic import context

import os
import sys
sys.path.append(os.getcwd())

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import config_by_env_name, ENV_NAME

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

import dotenv
dotenv.load_dotenv()

from db import Base
target_metadata = Base.metadata

from app.models.ingredient import Ingredient
from app.models.receipt import Receipt
from app.models.ingredients_receipts import IngredientsReceipts


def run_migrations_by_env_name(env_name):
    config = config_by_env_name[env_name]
    engine = create_engine(config.DATABASE_URL)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_migrations():
    run_migrations_by_env_name(ENV_NAME)

    if ENV_NAME == 'dev':
        run_migrations_by_env_name('test')


run_migrations()

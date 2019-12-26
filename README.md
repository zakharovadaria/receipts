[![Build Status](https://travis-ci.com/zakharovadaria/receipts.svg?branch=master)](https://travis-ci.com/zakharovadaria/receipts)
[![Coverage Status](https://coveralls.io/repos/github/zakharovadaria/receipts/badge.svg?branch=master)](https://coveralls.io/github/zakharovadaria/receipts?branch=master)

# Run tests

- python -m pytest

# Run migrations

- alembic upgrade head

# Make migration
##### Необходимо, чтобы файл был исполняемым
- ./makemigration.sh -m <name-of-migration>

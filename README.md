#Run tests

- python -m pytest

#Run migrations

- alembic upgrade head

#Make migration
#####Необходимо, чтобы файл был исполняемым
- ./makemigration.sh -m <name-of-migration>

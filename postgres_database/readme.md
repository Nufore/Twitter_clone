docker exec -it postgres_database-postgres-1 /bin/sh  

psql -U admin

\
**alembic commands:**

alembic upgrade head - создать миграцию

alembic downgrade -1 - откатить миграцию

alembic revision -m "create users table"

alembic revision --autogenerate -m "create users table" 
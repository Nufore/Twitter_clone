FROM python:3.11.8-slim

ADD ../requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD main.py /app/main.py
ADD models.py /app/models.py

WORKDIR /app

RUN alembic init alembic
COPY alembic.ini /app/alembic.ini
COPY alembic/env.py /app/alembic/env.py


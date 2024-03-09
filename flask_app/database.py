from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost"

engine = create_engine(DATABASE_URL, echo=True)
create_session = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
session = create_session()
Base = declarative_base()

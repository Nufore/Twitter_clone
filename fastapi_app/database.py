from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declarative_base, DeclarativeBase


DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
session = async_session()


class Base(AsyncAttrs, DeclarativeBase):
    pass


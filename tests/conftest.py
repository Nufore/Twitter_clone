from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from app.core.models import User
from app.core.models.base import Base
from app.core.models.db_helper import DatabaseHelper, db_helper
from app.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://admin:admin@localhost/test"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

db_helper_test = DatabaseHelper(url=DATABASE_URL_TEST, echo=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[db_helper.scoped_session_dependency] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
async def prepare_db_create_user():
    async with async_session_maker() as session:
        new_user = User(name="test_user", api_key="test")
        another_user = User(name="qwerty_user", api_key="qwerty")
        session.add_all([new_user, another_user])
        await session.commit()


transport = ASGITransport(app=app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://localhost:8000/") as ac:
        yield ac

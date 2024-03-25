import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from main import app
from core.models import User
from core.models.base import Base
from core.models.db_helper import DatabaseHelper, db_helper

DATABASE_URL_TEST = f"postgresql+asyncpg://admin:admin@localhost/test"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


db_helper_test = DatabaseHelper(url=DATABASE_URL_TEST, echo=False)

app.dependency_overrides[db_helper] = db_helper_test


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
        session.add(new_user)
        await session.commit()


transport = ASGITransport(app=app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://localhost:8000/") as ac:
        yield ac

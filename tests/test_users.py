import pytest
from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker, db_helper_test
from core.models.user import User


# @pytest.mark.anyio
async def test_create_user():
    async with async_session_maker() as session:
        name = "qwe_user"
        api_key = "qwe"

        new_user = User(name=name, api_key=api_key)
        session.add(new_user)
        await session.commit()

        query = select(User).order_by(-User.id).limit(1)
        user_from_db = await session.scalar(query)
        assert user_from_db.api_key == api_key, "Пользователь не добавился"


# async def test_get_tweets(ac: AsyncClient):
#     response = await ac.get("/api/tweets/", headers={"Api-Key": "test"})
#
#     assert response.status_code == 200

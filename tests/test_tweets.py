import pytest
from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker, db_helper_test
from core.models.user import User


async def test_get_tweets(ac: AsyncClient):
    response = await ac.get("http://127.0.0.1:8000/api/tweets/", headers={"Api-Key": "test"})

    assert response.status_code == 200

import pytest
from conftest import async_session_maker
from httpx import AsyncClient
from sqlalchemy import select

from app.core.models import User


@pytest.mark.asyncio(scope="session")
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


@pytest.mark.asyncio(scope="session")
async def test_get_user_by_id(ac: AsyncClient):
    user_id = 2
    response = await ac.get(
        f"/api/users/{user_id}",
        headers={"Api-Key": "test"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["user"]["id"] == user_id
    assert data["result"]


@pytest.mark.asyncio(scope="session")
async def test_get_user_by_wrong_id(ac: AsyncClient):
    user_id = 100 * 100
    response = await ac.get(
        f"/api/users/{user_id}",
        headers={"Api-Key": "test"},
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == f"User {user_id} not found."


@pytest.mark.asyncio(scope="session")
async def test_get_user_me(ac: AsyncClient):
    response = await ac.get("/api/users/me", headers={"Api-Key": "test"})
    data = response.json()
    assert response.status_code == 200
    assert data["user"]["name"] == "test_user"
    assert data["result"]


@pytest.mark.asyncio(scope="session")
async def test_get_user_me_wrong_api_key(ac: AsyncClient):
    api_key = "wrong_api_key"
    response = await ac.get("/api/users/me", headers={"Api-Key": api_key})
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == f"User with Api-Key='{api_key}' not found."


@pytest.mark.asyncio(scope="session")
async def test_follow_user(ac: AsyncClient):
    user_id = 2
    response = await ac.post(
        f"/api/users/{user_id}/follow",
        headers={"Api-Key": "test"},
    )
    result = response.json()["result"]
    assert response.status_code == 201
    assert result


@pytest.mark.asyncio(scope="session")
async def test_follow_user_wrong_id(ac: AsyncClient):
    user_id = 2 * 1000
    response = await ac.post(
        f"/api/users/{user_id}/follow",
        headers={"Api-Key": "test"},
    )
    result = response.json()
    assert response.status_code == 404
    assert result["detail"] == f"User {user_id} not found."


@pytest.mark.asyncio(scope="session")
async def test_follow_user_again(ac: AsyncClient):
    user_id = 2
    response = await ac.post(
        f"/api/users/{user_id}/follow",
        headers={"Api-Key": "test"},
    )
    result = response.json()["result"]
    assert response.status_code == 200
    assert not result


@pytest.mark.asyncio(scope="session")
async def test_unfollow_user(ac: AsyncClient):
    user_id = 2
    response = await ac.delete(
        f"/api/users/{user_id}/follow",
        headers={"Api-Key": "test"},
    )
    result = response.json()["result"]
    assert response.status_code == 200
    assert result

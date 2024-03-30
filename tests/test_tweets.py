import pytest
from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker
from app.core.models.tweet import Tweet


@pytest.mark.asyncio(scope="session")
async def test_get_tweets(ac: AsyncClient):
    response = await ac.get("/api/tweets/", headers={"Api-Key": "test"})
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_create_tweet(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = select(Tweet).order_by(-Tweet.id).limit(1)
        tweet_from_db = await session.scalar(stmt)
    last_tweet_id = 0
    if tweet_from_db:
        last_tweet_id = tweet_from_db.id

    data = {
        "tweet_data": "test_tweet_1",
        "tweet_media_ids": [],
    }
    response = await ac.post(
        "/api/tweets/",
        headers={"Api-Key": "test"},
        json=data,
    )
    current_tweet_id = response.json()["tweet_id"]
    assert response.status_code == 201
    assert current_tweet_id == last_tweet_id + 1


@pytest.mark.asyncio(scope="session")
async def test_create_like(ac: AsyncClient):
    tweet_id = 1
    response = await ac.post(
        f"/api/tweets/{tweet_id}/likes", headers={"Api-Key": "test"}
    )
    result = response.json()["result"]
    assert response.status_code == 201
    assert result


@pytest.mark.asyncio(scope="session")
async def test_create_like_already_exists(ac: AsyncClient):
    tweet_id = 1
    response = await ac.post(
        f"/api/tweets/{tweet_id}/likes", headers={"Api-Key": "test"}
    )
    result = response.json()["result"]
    message = response.json()["message"]
    assert response.status_code == 400
    assert not result
    assert message == "Like is already exists"


@pytest.mark.asyncio(scope="session")
async def test_delete_like_by_wrong_user(ac: AsyncClient):
    tweet_id = 1
    response = await ac.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"Api-Key": "qwerty"}
    )
    result = response.json()["result"]
    message = response.json()["message"]
    assert response.status_code == 400
    assert not result
    assert message == "There is not like on that tweet"


@pytest.mark.asyncio(scope="session")
async def test_delete_like(ac: AsyncClient):
    tweet_id = 1
    response = await ac.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"Api-Key": "test"}
    )
    result = response.json()["result"]
    assert response.status_code == 200
    assert result


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_by_wrong_user(ac: AsyncClient):
    tweet_id = 1
    api_key = "qwerty"
    response = await ac.delete(f"/api/tweets/{tweet_id}", headers={"Api-Key": api_key})
    detail = response.json()["detail"]
    assert response.status_code == 404
    assert detail == f"Tweet {tweet_id} by user <{api_key}> not found."


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet(ac: AsyncClient):
    tweet_id = 1
    response = await ac.delete(f"/api/tweets/{tweet_id}", headers={"Api-Key": "test"})
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_without_api_key(ac: AsyncClient):
    tweet_id = 1
    response = await ac.delete(f"/api/tweets/{tweet_id}")
    assert response.status_code == 422

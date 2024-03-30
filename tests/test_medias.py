import pytest
from sqlalchemy import select
from httpx import AsyncClient

from app.core.config import BASE_DIR
from app.core.models.media import Media
from conftest import async_session_maker


test_file = BASE_DIR / "tests" / "test_image.jpg"
FILES = {"file": open(test_file, "rb")}


@pytest.mark.asyncio(scope="session")
async def test_post_media(ac: AsyncClient):

    async with async_session_maker() as session:
        stmt = select(Media).order_by(-Media.id).limit(1)
        media_from_db = await session.scalar(stmt)
    last_media_id = 0
    if media_from_db:
        last_media_id = media_from_db.id

    response = await ac.post("/api/medias/", files=FILES)
    current_media_id = response.json()["media_id"]

    assert response.status_code == 201
    assert current_media_id == last_media_id + 1

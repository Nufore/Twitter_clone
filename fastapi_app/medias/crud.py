from core.models import Media
from sqlalchemy.ext.asyncio import AsyncSession


async def create_media(session: AsyncSession, path: str):
    new_media = Media(path=path)
    session.add(new_media)
    await session.commit()
    return {
        "result": True,
        "media_id": new_media.id
    }

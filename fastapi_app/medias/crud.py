from core.models import Media
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings


async def create_media(session: AsyncSession, path: str):
    new_media = Media(path=f"{settings.file_save_prefix}{path}")
    session.add(new_media)
    await session.commit()
    return {"result": True, "media_id": new_media.id}

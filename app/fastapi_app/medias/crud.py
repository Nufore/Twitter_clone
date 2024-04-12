import os
import time

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename

from app.core.config import settings
from app.core.models import Media


async def create_media(session: AsyncSession, path: str):
    new_media = Media(path=f"{settings.file_save_prefix}{path}")
    session.add(new_media)
    await session.commit()
    return {"result": True, "media_id": new_media.id}


async def save_media_file(file: UploadFile):
    filename = secure_filename(f"{time.time()}_{file.filename}")
    content = await file.read()

    async with aiofiles.open(os.path.join(settings.static_image_dir, filename), "wb") as f:
        await f.write(content)

    return filename

from fastapi import UploadFile
from werkzeug.utils import secure_filename
from sqlalchemy.ext.asyncio import AsyncSession

import os
import time

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
    with open(os.path.join(settings.image_dir, filename), "wb") as f:
        f.write(content)
        f.close()
    return filename

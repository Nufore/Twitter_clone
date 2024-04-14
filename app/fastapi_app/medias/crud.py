import os
import time

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename

from app.core.config import settings
from app.core.models import Media


async def create_media(session: AsyncSession, path: str) -> dict:
    """
    Функция записи данных по файлу в БД.

    :param session: Асинхронная сессия
    :param path: путь до файла

    :return: возвращаем словарь с результатом и id файла в БД
    """
    new_media = Media(path=f"{settings.file_save_prefix}{path}")
    session.add(new_media)
    await session.commit()
    return {"result": True, "media_id": new_media.id}


async def save_media_file(file: UploadFile) -> str:
    """
    Функция сохранения файла в хранилище.

    :param file: Данные по файлу

    :return: возвращаем название файла после его сохранения
    """
    filename = secure_filename(f"{time.time()}_{file.filename}")
    content = await file.read()

    file_to_write = os.path.join(settings.static_image_dir, filename)

    async with aiofiles.open(file_to_write, "wb") as fw:
        await fw.write(content)

    return filename

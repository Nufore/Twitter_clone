from fastapi import APIRouter, status, Request, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename
import os

from core.models import db_helper
from core.config import settings
from . import crud

router = APIRouter(tags=["Medias"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_media(
    request: Request,
    file: UploadFile,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    filename = secure_filename(file.filename)
    content = await file.read()
    with open(os.path.join(settings.image_dir, filename), "wb") as f:
        f.write(content)
        f.close()

    return await crud.create_media(session=session, path=filename)


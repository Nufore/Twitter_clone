from fastapi import APIRouter, status, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import db_helper
from . import crud

router = APIRouter(tags=["Medias"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_media(
    file: UploadFile,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    filename = await crud.save_media_file(file=file)
    return await crud.create_media(session=session, path=filename)


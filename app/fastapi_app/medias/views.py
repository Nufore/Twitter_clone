from fastapi import APIRouter, Depends, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper

from . import crud
from .schemas import FileSchema

router = APIRouter(tags=["Medias"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Загрузка изображений к твиту",
    description="Проверка расширения файла и загрузка изображений к твиту",
)
async def post_media(
    file: UploadFile,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    file_data = FileSchema(
        filename=file.filename,
        content_type=file.content_type,
    )
    result = file_data.check_content_type()
    if result["result"]:
        filename = await crud.save_media_file(file=file)
        return await crud.create_media(session=session, path=filename)

    response.status_code = status.HTTP_400_BAD_REQUEST
    return result

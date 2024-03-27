from fastapi import APIRouter, status, Depends, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper
from .schemas import FileSchema

router = APIRouter(tags=["Medias"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_media(
    file: UploadFile,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    file_data = FileSchema(filename=file.filename, content_type=file.content_type)
    result = file_data.check_content_type()
    if result["result"]:
        filename = await crud.save_media_file(file=file)
        return await crud.create_media(session=session, path=filename)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

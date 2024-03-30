from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, User
from . import crud


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found.",
    )


async def user_by_apikey(
    api_key: Annotated[str, Header()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user_by_api_key(session=session, api_key=api_key)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with Api-Key = <{api_key}> not found.",
    )

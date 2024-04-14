from typing import Annotated

from fastapi import Depends, Header, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper

from . import crud


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    """
    Получение данных пользователя по его id для зависимости во views.

    :param user_id: id пользователя
    :param session: Асинхронная сессия

    :return: возвращаем данные по пользователю
    или сообщение о том, что такого пользователя нет
    """
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
    """
    Получение данных пользователя
    по переданному API-ключу для зависимости во views.

    :param api_key: API-ключ переданный в headers при запросе
    :param session: Асинхронная сессия

    :return: возвращаем данные по пользователю
    или сообщение о том, что пользователя с таким ключом нет
    """
    user = await crud.get_user_by_api_key(session=session, api_key=api_key)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with Api-Key = <{api_key}> not found.",
    )

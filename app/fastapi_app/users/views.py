from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper

from . import crud
from .dependencies import user_by_apikey, user_by_id
from .schemas import ResponseFollowUser, ResponseUser

router = APIRouter(tags=["Users"])


@router.post(
    "/{user_id}/follow",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseFollowUser,
    summary="Подписаться на другого пользователя",
    description="Находим текущего пользователя по предоставленному API-ключу "
                "и подписываемся на переданного по user_id",
)
async def follow_user(
        response: Response,
        user: User = Depends(user_by_apikey),
        user_to_follow: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.follow_user(
        session=session,
        user=user,
        user_to_follow=user_to_follow,
    )
    if not res["result"]:
        response.status_code = status.HTTP_200_OK
    return res


@router.delete(
    "/{user_id}/follow",
    status_code=status.HTTP_200_OK,
    response_model=ResponseFollowUser,
    summary="Убрать подписку на другого пользователя",
    description="Находим текущего пользователя по предоставленному API-ключу "
                "и убираем подписку с переданного по user_id",
)
async def unfollow_user(
        user: User = Depends(user_by_apikey),
        user_to_unfollow: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.unfollow_user(
        session=session,
        user=user,
        user_to_unfollow=user_to_unfollow,
    )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUser,
    summary="Получить информацию о своём профиле",
    description="Находим пользователя по предоставленному API-ключу",
)
async def get_user_me(
        user: User = Depends(user_by_apikey),
):
    return await crud.get_user_data(user=user)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUser,
    summary="Получить информацию о произвольном профиле по его id",
    description="Находим пользователя по предоставленному id",
)
async def get_user(
        user: User = Depends(user_by_id),
):
    return await crud.get_user_data(user=user)

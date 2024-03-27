from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from . import crud
from .dependencies import user_by_id, user_by_apikey

router = APIRouter(tags=["Users"])


@router.post("/{user_id}/follow", status_code=status.HTTP_201_CREATED)
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


@router.delete("/{user_id}/follow", status_code=status.HTTP_200_OK)
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


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(
    user: User = Depends(user_by_apikey),
):
    return await crud.get_user_data(user=user)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user: User = Depends(user_by_id),
):
    return await crud.get_user_data(user=user)

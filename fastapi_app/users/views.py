from fastapi import APIRouter, status, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User as User_
from . import crud
from .schemas import User, UserCreate, UserUpdate, UserUpdatePartial
from .dependencies import user_by_id

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.put("/{user_id}")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(session=session, user=user, user_update=user_update)


@router.patch("/{user_id}")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session, user=user, user_update=user_update, partial=True
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_user(session=session, user=user)


@router.post("/{user_id}/follow", status_code=status.HTTP_201_CREATED)
async def follow_user(
    request: Request,
    user_to_follow: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")

    res = await crud.follow_user(
        session=session, api_key=api_key, user_to_follow=user_to_follow
    )

    return {"result": res}


@router.delete("/{user_id}/follow", status_code=status.HTTP_200_OK)
async def unfollow_user(
    request: Request,
    user_to_unfollow: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")

    res = await crud.unfollow_user(
        session=session, api_key=api_key, user_to_unfollow=user_to_unfollow
    )

    return {"result": res}


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")

    res = await crud.get_user_data(session=session, api_key=api_key)
    return res


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.get_user_data(session=session, user_id=user.id)
    return res

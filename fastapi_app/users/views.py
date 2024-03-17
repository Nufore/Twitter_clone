from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
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


@router.get("/{user_id}", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user


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
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")
    user_me = await crud.get_user_by_api_key(session=session, api_key=api_key)

    await user_me.follow(user=user, session=session)

    return {"result": True}


@router.delete("/{user_id}/follow", status_code=status.HTTP_200_OK)
async def unfollow_user(
    request: Request,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")
    user_me = await crud.get_user_by_api_key(session=session, api_key=api_key)

    await user_me.unfollow(user=user, session=session)

    return {"result": True}

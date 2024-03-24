from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, followers


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    stmt = (
        select(User)
        .options(joinedload(User.followed), joinedload(User.followers))
        .where(User.id == user_id)
    )
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User | None:
    stmt = (
        select(User)
        .options(joinedload(User.followed), joinedload(User.followers))
        .where(User.api_key == api_key)
    )
    user: User | None = await session.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with Api-Key='{api_key}' not found.",
        )
    return user


def is_followed(
    user: User,
    user_to_follow: User,
):
    if user_to_follow in user.followed or user.id == user_to_follow.id:
        return True
    return False


async def follow_user(
    session: AsyncSession,
    user: User,
    user_to_follow: User,
):
    if not is_followed(user=user, user_to_follow=user_to_follow):
        user.followed.append(user_to_follow)
        await session.commit()
        return {"result": True}
    return {"result": False}


async def unfollow_user(
    session: AsyncSession,
    user: User,
    user_to_unfollow: User,
):
    if is_followed(user=user, user_to_follow=user_to_unfollow):
        user.followed.remove(user_to_unfollow)
        await session.commit()
        return {"result": True}
    return {"result": False}


async def get_user_data(user: User) -> dict | None:
    data = {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [usr.id_name_to_json() for usr in user.followers],
            "following": [usr.id_name_to_json() for usr in user.followed],
        },
    }
    return data

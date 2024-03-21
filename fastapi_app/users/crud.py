from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User, followers
from .schemas import UserCreate, UserUpdate, UserUpdatePartial


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User | None:
    stmt = select(User).where(User.api_key == api_key)
    user: User | None = await session.scalar(stmt)
    return user


async def is_followed(session: AsyncSession, user_me: User, user_to_follow: User):
    stmt = select(followers).filter(
        followers.c.follower_id == user_me.id,
        followers.c.followed_id == user_to_follow.id,
    )
    result = await session.execute(stmt)
    is_follow = result.scalars().all()
    if is_follow:
        return True
    return False


async def follow_user(session: AsyncSession, api_key: str, user_to_follow: User):
    stmt = (
        select(User).options(joinedload(User.followed)).where(User.api_key == api_key)
    )
    user_me = await session.scalar(stmt)
    if not await is_followed(
        session=session, user_me=user_me, user_to_follow=user_to_follow
    ):
        user_me.followed.append(user_to_follow)
        await session.commit()
        return True
    return False


async def unfollow_user(session: AsyncSession, api_key: str, user_to_unfollow: User):
    stmt = (
        select(User).options(joinedload(User.followed)).where(User.api_key == api_key)
    )
    user_me = await session.scalar(stmt)
    if await is_followed(
        session=session, user_me=user_me, user_to_follow=user_to_unfollow
    ):
        user_me.followed.remove(user_to_unfollow)
        await session.commit()
        return True
    return False


async def get_user_data(
    session: AsyncSession, api_key: str | None = None, user_id: int | None = None
) -> dict | None:
    if api_key:
        stmt = (
            select(User)
            .options(joinedload(User.followed), joinedload(User.followers))
            .where(User.api_key == api_key)
        )
    else:
        stmt = (
            select(User)
            .options(joinedload(User.followed), joinedload(User.followers))
            .where(User.id == user_id)
        )
    user = await session.scalar(stmt)
    if user:
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
    return {"result": False}

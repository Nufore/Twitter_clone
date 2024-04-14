from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.models import User


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """
    Получение пользователя по его id.

    :param session: Асинхронная сессия
    :param user_id: id пользователя в БД

    :return: возвращаем данные по пользователю из БД
    или None если такой пользователь не найден
    """
    stmt = (
        select(User)
        .options(joinedload(User.followed), joinedload(User.followers))
        .where(User.id == user_id)
    )
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_by_api_key(
    session: AsyncSession,
    api_key: str,
) -> User:
    """
    Получение пользователя(вместе с подписками и подписчиками)
    по переданному API-ключу.

    :param session: Асинхронная сессия
    :param api_key: API-ключ, переданный в headers при запросе

    :return: возвращаем данные по пользователю из БД
    или выбрасываем ошибку о том, что такой пользователь не найден
    """
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
    """
    Проверка подписки одного пользователя на другого.

    Также идет проверка подписки самого на себя -
    в данному случае возвращаем True,
    чтобы не подписываться на себя в функции follow_user

    :param user: Пользователь, который подписывается
    :param user_to_follow: Пользователь на которого подписываются

    :return: возвращаем True или False в зависимости от проверки
    """
    return user_to_follow in user.followed or user.id == user_to_follow.id


async def follow_user(
    session: AsyncSession,
    user: User,
    user_to_follow: User,
):
    """
    Подписаться на пользователя,
    предварительно проверив нет ли уже подписки на данного пользователя.

    :param session: Асинхронная сессия
    :param user: Пользователь, который подписывается
    :param user_to_follow: Пользователь на которого подписываются

    :return: словарь с "result" True или False - результат выполнения
    """
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
    """
    Убрать подписку на другого пользователя,
    предварительно проверив, что такая подписка есть.

    :param session: Асинхронная сессия
    :param user: Пользователь, который хочет убрать подписку
    :param user_to_unfollow: Пользователь с которого убирают подписку

    :return: словарь с "result" True или False - результат выполнения
    """
    if is_followed(user=user, user_to_follow=user_to_unfollow):
        user.followed.remove(user_to_unfollow)
        await session.commit()
        return {"result": True}
    return {"result": False}


async def get_user_data(user: User) -> dict | None:
    """
    Получить данные по пользователю.

    :param user: Пользователь

    :return: словарь с данными по пользователю
    """
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [usr.id_name_to_json() for usr in user.followers],
            "following": [usr.id_name_to_json() for usr in user.followed],
        },
    }

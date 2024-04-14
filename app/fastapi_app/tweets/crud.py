from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.models import Like, Media, Tweet, User

from .schemas import TweetCreate


async def create_tweet(
    session: AsyncSession,
    tweet_in: TweetCreate,
    user_id: int,
):
    """
    Создание нового твита.

    :param session: Асинхронная сессия
    :param tweet_in: Данные нового твита
    :param user_id: Пользователь, создающий твит

    :return: возвращаем словарь с результатом выполнения и id твита
    """
    tweet = Tweet(tweet_data=tweet_in.tweet_data, user_id=user_id)
    session.add(tweet)
    await session.commit()

    if tweet_in.tweet_media_ids:
        for media_id in tweet_in.tweet_media_ids:
            stmt = select(Media).where(Media.id == media_id)
            media_file = await session.scalar(stmt)
            if media_file:
                media_file.tweet_id = tweet.id

        await session.commit()
    return {"result": True, "tweet_id": tweet.id}


async def get_tweet(session: AsyncSession, tweet_id: int) -> Tweet | None:
    """
    Получение твита по переданному id.

    :param session: Асинхронная сессия
    :param tweet_id: id твита

    :return: возвращаем твит
    или None если ничего не нашли
    """
    return await session.get(Tweet, tweet_id)


async def get_tweets(session: AsyncSession, user: User) -> dict | None:
    """
    Получение ленты твитов.

    :param session: Асинхронная сессия
    :param user: Пользователь полученный по API-ключу в запросе

    :return: возвращаем словарь с результатом и списком твитов
    """
    if settings.upload_all_tweets:
        stmt = (
            select(Tweet).
            options(
                selectinload(Tweet.likes).subqueryload(Like.user),
                selectinload(Tweet.user),
                selectinload(Tweet.medias),
            ).
            order_by(-Tweet.id)
        )
    else:
        stmt = (
            select(Tweet).
            options(
                selectinload(Tweet.likes).subqueryload(Like.user),
                selectinload(Tweet.user),
                selectinload(Tweet.medias),
            ).
            filter(
                or_(
                    Tweet.user_id.in_(flwr.id for flwr in user.followed),
                    Tweet.user_id == user.id,
                )
            ).
            order_by(-Tweet.id)
        )
    res = await session.scalars(stmt)

    tweets = res.all()

    return {
        "result": True,
        "tweets": [tweet.to_json() for tweet in tweets],
    }


async def delete_tweet(session: AsyncSession, tweet: Tweet) -> dict:
    """
    Удаление твита.

    :param session: Асинхронная сессия
    :param tweet: Твит

    :return: возвращаем результат удаления
    """
    await session.delete(tweet)
    await session.commit()
    return {"result": True}


async def create_like(
    session: AsyncSession,
    tweet_id: int,
    user_id: int,
) -> dict:
    """
    Поставить отметку «Нравится» на твит,
    предварительно проверив наличие лайка.

    :param session: Асинхронная сессия
    :param tweet_id: id твита
    :param user_id: id пользователя

    :return: возвращаем результат выполнения
    """
    if await is_like_on_tweet_exists(
        session=session,
        tweet_id=tweet_id,
        user_id=user_id,
    ):
        return {"result": False}
    new_like = Like(user_id=user_id, tweet_id=tweet_id)
    session.add(new_like)
    await session.commit()
    return {"result": True}


async def delete_like(
    session: AsyncSession,
    tweet_id: int,
    user_id: int,
) -> dict:
    """
    Убрать отметку «Нравится» с твита,
    предварительно проверив наличие лайка.

    :param session: Асинхронная сессия
    :param tweet_id: id твита
    :param user_id: id пользователя

    :return: возвращаем результат выполнения
    """
    like = await is_like_on_tweet_exists(
        session=session,
        tweet_id=tweet_id,
        user_id=user_id,
    )
    if not like:
        return {"result": False}
    await session.delete(like)
    await session.commit()
    return {"result": True}


async def is_like_on_tweet_exists(
    session: AsyncSession,
    tweet_id: int,
    user_id: int,
) -> Like | None:
    """
    Проверяем наличие лайка на твите от пользователя.

    :param session: Асинхронная сессия
    :param tweet_id: id твита
    :param user_id: id пользователя

    :return: возвращаем лайк или None
    """
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.tweet_id == tweet_id,
    )
    return await session.scalar(stmt)

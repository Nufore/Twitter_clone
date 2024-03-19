from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TweetCreate
from core.models import Tweet, Like


async def create_tweet(session: AsyncSession, tweet_in: TweetCreate):
    tweet = Tweet(**tweet_in.model_dump())
    session.add(tweet)
    await session.commit()
    return {"tweet_id": tweet.id}


async def get_tweet(session: AsyncSession, tweet_id: int) -> Tweet | None:
    return await session.get(Tweet, tweet_id)


async def delete_tweet(session: AsyncSession, tweet_id: int, user_id: int):
    stmt = select(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id)
    tweet: Tweet | None = await session.scalar(stmt)
    if tweet:
        await session.delete(tweet)
        await session.commit()
        return True
    return False


async def create_like(session: AsyncSession, tweet_id: int, user_id: int):
    stmt = select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
    is_exists: Like | None = await session.scalar(stmt)
    if is_exists:
        return {"result": False}
    new_like = Like(user_id=user_id, tweet_id=tweet_id)
    session.add(new_like)
    await session.commit()
    return {"result": True}


async def delete_like(session: AsyncSession, tweet_id: int, user_id: int):
    stmt = select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
    like: Like | None = await session.scalar(stmt)
    if not like:
        return {"result": False}
    await session.delete(like)
    await session.commit()
    return {"result": True}

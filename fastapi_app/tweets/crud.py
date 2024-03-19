from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TweetCreate
from core.models import Tweet


async def create_tweet(session: AsyncSession, tweet_in: TweetCreate):
    tweet = Tweet(**tweet_in.model_dump())
    session.add(tweet)
    await session.commit()
    return {"tweet_id": tweet.id}


async def get_tweet(session: AsyncSession, tweet_id: int) -> Tweet | None:
    return await session.get(Tweet, tweet_id)


async def delete_tweet(session: AsyncSession, tweet_id, user_id):
    stmt = select(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id)
    tweet: Tweet | None = await session.scalar(stmt)
    if tweet:
        await session.delete(tweet)
        await session.commit()
        return True
    return False

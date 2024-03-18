from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TweetCreate
from core.models import Tweet, User


async def create_tweet(session: AsyncSession, tweet_in: TweetCreate):
    tweet = Tweet(**tweet_in.model_dump())
    session.add(tweet)
    await session.commit()
    return {"tweet_id": tweet.id}

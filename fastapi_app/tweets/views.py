from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Tweet, User
from .dependencies import tweet_by_id, tweet_for_delete
from .schemas import TweetCreate
from . import crud
from ..users import dependencies as user_dependencies

router = APIRouter(tags=["Tweets"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet_in: TweetCreate,
    user: User = Depends(user_dependencies.user_by_apikey),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_tweet(session=session, tweet_in=tweet_in, user_id=user.id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tweets(
    user: User = Depends(user_dependencies.user_by_apikey),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_tweets(session=session, user=user)


@router.delete("/{tweet_id}", status_code=status.HTTP_200_OK)
async def delete_tweet(
    tweet: Tweet = Depends(tweet_for_delete),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_tweet(session=session, tweet=tweet)


@router.post("/{tweet_id}/likes", status_code=status.HTTP_201_CREATED)
async def create_like(
    tweet: Tweet = Depends(tweet_by_id),
    user: User = Depends(user_dependencies.user_by_apikey),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_like(session=session, tweet_id=tweet.id, user_id=user.id)


@router.delete("/{tweet_id}/likes", status_code=status.HTTP_200_OK)
async def delete_like(
    tweet: Tweet = Depends(tweet_by_id),
    user: User = Depends(user_dependencies.user_by_apikey),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_like(session=session, tweet_id=tweet.id, user_id=user.id)

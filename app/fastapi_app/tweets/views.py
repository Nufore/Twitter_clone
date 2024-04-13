from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Tweet, User, db_helper

from ..users import dependencies as user_dependencies
from . import crud
from .dependencies import tweet_by_id, tweet_for_delete
from .schemas import TweetCreate

router = APIRouter(tags=["Tweets"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tweet(
        tweet_in: TweetCreate,
        user: User = Depends(user_dependencies.user_by_apikey),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_tweet(
        session=session,
        tweet_in=tweet_in,
        user_id=user.id,
    )


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
        response: Response,
        tweet: Tweet = Depends(tweet_by_id),
        user: User = Depends(user_dependencies.user_by_apikey),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.create_like(
        session=session,
        tweet_id=tweet.id,
        user_id=user.id,
    )
    if not res["result"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.delete("/{tweet_id}/likes", status_code=status.HTTP_200_OK)
async def delete_like(
        response: Response,
        tweet: Tweet = Depends(tweet_by_id),
        user: User = Depends(user_dependencies.user_by_apikey),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.delete_like(
        session=session,
        tweet_id=tweet.id,
        user_id=user.id,
    )
    if not res["result"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res

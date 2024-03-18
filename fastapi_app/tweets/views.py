from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import Tweet, TweetCreate, TweetToResponse
from . import crud
from ..users import crud as users_crud

router = APIRouter(tags=["Tweets"])


@router.post("/", response_model=TweetToResponse, status_code=status.HTTP_201_CREATED)
async def create_tweet(
    request: Request,
    tweet_in: TweetCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    api_key = request.headers.get("Api-Key")
    user = await users_crud.get_user_by_api_key(session=session, api_key=api_key)
    tweet_in.user_id = user.id
    return await crud.create_tweet(session=session, tweet_in=tweet_in)
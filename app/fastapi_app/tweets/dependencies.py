from typing import Annotated

from fastapi import Depends, Header, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Tweet, User, db_helper

from ..users import crud as user_crud
from . import crud


async def tweet_by_id(
        tweet_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Tweet:
    tweet = await crud.get_tweet(session=session, tweet_id=tweet_id)
    if tweet:
        return tweet

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tweet {tweet_id} not found.",
    )


async def tweet_for_delete(
        tweet_id: Annotated[int, Path],
        api_key: Annotated[str, Header()],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Tweet:
    user: User = await user_crud.get_user_by_api_key(
        session=session,
        api_key=api_key,
    )
    stmt = select(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user.id)
    tweet: Tweet | None = await session.scalar(stmt)

    if tweet:
        return tweet

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tweet {tweet_id} by user <{api_key}> not found.",
    )

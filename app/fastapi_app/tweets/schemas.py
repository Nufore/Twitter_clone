from pydantic import BaseModel, ConfigDict
from typing import List


class TweetBase(BaseModel):
    tweet_data: str
    user_id: int | None = None


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] | None = None


class Tweet(TweetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TweetToResponse(BaseModel):
    result: bool = True
    tweet_id: int

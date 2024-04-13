from typing import List, Optional

from pydantic import BaseModel, ConfigDict


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


class AuthorData(BaseModel):
    id: int
    name: str


class UserLikeData(BaseModel):
    user_id: int
    name: str


class TweetData(BaseModel):
    id: int
    content: str
    attachments: List[str] | None = ["link_1", "link_2"]
    author: AuthorData
    likes: List[UserLikeData] | None


class ResponseTweets(BaseModel):
    result: bool = True | False
    tweets: List[TweetData] | None


class ResponseActionTweet(BaseModel):
    result: bool = True | False

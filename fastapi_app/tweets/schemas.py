from pydantic import BaseModel, ConfigDict


class TweetBase(BaseModel):
    tweet_data: str
    user_id: int | None = None


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TweetToResponse(BaseModel):
    result: bool = True
    tweet_id: int

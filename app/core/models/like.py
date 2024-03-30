from .base import Base
from .mixins import UserRelationMixin, TweetRelationMixin

from sqlalchemy import UniqueConstraint


class Like(UserRelationMixin, TweetRelationMixin, Base):
    __tablename__ = "likes"

    _user_primary_key = True
    _user_back_populates = "likes"

    _tweet_primary_key = True
    _tweet_back_populates = "likes"

    UniqueConstraint("user_id", "tweet_id", name="unique_like")

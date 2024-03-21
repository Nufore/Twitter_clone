from typing import TYPE_CHECKING

from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from .user import User
    from .tweet import Tweet


class UserRelationMixin:
    _user_primary_key: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("users.id"), primary_key=cls._user_primary_key)

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User", back_populates=cls._user_back_populates)


class TweetRelationMixin:
    _tweet_primary_key: bool = False
    _tweet_back_populates: str | None = None
    _nullable: bool | None = None

    @declared_attr
    def tweet_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("tweets.id"), primary_key=cls._tweet_primary_key, nullable=cls._nullable)

    @declared_attr
    def tweet(cls) -> Mapped["Tweet"]:
        return relationship("Tweet", back_populates=cls._tweet_back_populates)

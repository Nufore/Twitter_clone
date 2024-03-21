from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User
    from .like import Like
    from .media import Media


class Tweet(UserRelationMixin, Base):
    __tablename__ = "tweets"
    _user_back_populates = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tweet_data: Mapped[str] = mapped_column(Text, nullable=False)

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship(back_populates="tweets")

    likes: Mapped[list["Like"]] = relationship(back_populates="tweet", cascade="all, delete-orphan")
    medias: Mapped[list["Media"]] = relationship(back_populates="tweet", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.tweet_data,
            "attachments": [],  # [media.path for media in self.medias],
            "author": self.user.id_name_to_json(),
            "likes": [like.user.id_name_to_json() for like in self.likes],
        }

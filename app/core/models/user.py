from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .like import Like
    from .tweet import Tweet


followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    api_key: Mapped[str] = mapped_column(Text, unique=True)

    followed: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        back_populates="followers",
    )
    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.followed_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates="followed",
    )

    tweets: Mapped[list["Tweet"]] = relationship(back_populates="user")
    likes: Mapped[list["Like"]] = relationship(back_populates="user")

    def id_name_to_json(self):
        return {"id": self.id, "name": self.name}

    def user_id_name_to_json(self):
        return {"user_id": self.id, "name": self.name}

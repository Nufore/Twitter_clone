from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, ForeignKey, Integer, Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .base import Base

if TYPE_CHECKING:
    from .tweet import Tweet
    from .like import Like


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

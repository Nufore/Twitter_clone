from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List
from .base import Base

if TYPE_CHECKING:
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
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    tweets: Mapped[list["Tweet"]] = relationship(back_populates="user")

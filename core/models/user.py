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
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    tweets: Mapped[list["Tweet"]] = relationship(back_populates="user")
    likes: Mapped[list["Like"]] = relationship(back_populates="user")

    async def follow(self, user: "User", session: AsyncSession):
        if not await self.is_followed(user=user, session=session):
            self.followed.append(user)
            await session.commit()

    async def unfollow(self, user: "User", session: AsyncSession):
        if await self.is_followed(user=user, session=session):
            self.followed.remove(user)
            await session.commit()

    async def is_followed(self, user: "User", session: AsyncSession):
        stmt = select(followers).filter(followers.c.follower_id == self.id, followers.c.followed_id == user.id)
        result = await session.execute(stmt)
        is_follow = result.scalars().all()
        if is_follow:
            return True
        return False

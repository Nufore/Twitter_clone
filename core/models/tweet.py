from .base import Base
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

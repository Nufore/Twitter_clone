from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import TweetRelationMixin


class Media(TweetRelationMixin, Base):
    __tablename__ = "medias"
    _tweet_back_populates = "medias"
    _nullable = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    path: Mapped[str]

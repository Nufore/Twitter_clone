from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from database import Base


followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    api_key = Column(Text, unique=True)
    followed = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def id_name_to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="tweets")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "attachments": [],
            "author": self.user.id_name_to_json(),
            "likes": [like.user.id_name_to_json() for like in self.likes]
        }


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", backref="likes")

    tweet_id = Column(Integer, ForeignKey("tweets.id"), primary_key=True)
    tweet = relationship("Tweet", backref="likes")

    UniqueConstraint("user_id", "tweet_id", name="unique_like")

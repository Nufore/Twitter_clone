from typing import List

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    api_key: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    name: str | None = None
    api_key: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ResponseFollowUser(BaseModel):
    result: bool = True | False


class Follow(BaseModel):
    id: int
    name: str


class UserData(BaseModel):
    id: int
    name: str
    followers: List[Follow]
    following: List[Follow]


class ResponseUser(BaseModel):
    result: bool = True | False
    user: UserData

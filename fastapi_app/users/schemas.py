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

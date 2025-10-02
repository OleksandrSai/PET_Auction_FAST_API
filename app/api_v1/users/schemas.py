from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    login: str
    name: Optional[str]


class UserCreate(UserBase):
    password: str
    pass

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    login: Optional[str]
    password: Optional[str]
    name: Optional[str]


class UserPublic(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

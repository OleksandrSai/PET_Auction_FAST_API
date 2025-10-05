from pydantic import ConfigDict
from typing import Optional
from api_v1.base_schema import BaseUser


class UserCreate(BaseUser):
    password: str
    balance: float
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    login: Optional[str]
    password: Optional[str]
    name: Optional[str]
    balance: Optional[float]


class UserPublic(BaseUser):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

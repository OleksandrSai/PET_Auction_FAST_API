from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    login: str
    password: str
    name: Optional[str]


class UserCreate(BaseModel):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

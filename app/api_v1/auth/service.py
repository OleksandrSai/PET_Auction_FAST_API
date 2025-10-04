from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select

from api_v1.users.schema import UserPublic
from utils.security import validate_password
from core import db_helper
from core.models import User


async def validate_user(
    login: str,
    password: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserPublic | None:

    user = (
        await session.execute(select(User).filter_by(login=login))
    ).scalar_one_or_none()

    if not user or not validate_password(
        password=password, hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return user

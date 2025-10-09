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
from utils.security import decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from utils.enums import TokenType


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


async def refresher_token(
        refresh_token: str,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserPublic | None:

    if refresh_token.startswith("Bearer "):
        refresh_token = refresh_token.removeprefix("Bearer ").strip()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    decoded_refresh = decode_jwt(refresh_token)

    if decoded_refresh.get("type") != TokenType.REFRESH:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a refresh token",
        )

    user_id = int(decoded_refresh.get("sub"))

    user = await session.get(User, user_id)
    return UserPublic(
        id=user.id,
        login=user.login,
        name=user.name
    )



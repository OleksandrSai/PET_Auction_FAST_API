from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from api_v1.users.schemas import UserPublic
from utils.security import validate_password
from core import db_helper
from core.models import User
from datetime import datetime, timedelta
import jwt
from core.config import settings


async def validate_user(
    login: str,
    password: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User | None:
    auth_failed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

    if not (
        user := (
            await session.execute(select(User).filter_by(login=login))
        ).scalar_one_or_none()
    ):
        raise auth_failed_exc

    if not validate_password(password=password, hashed_password=user.password):
        raise auth_failed_exc

    return user


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded

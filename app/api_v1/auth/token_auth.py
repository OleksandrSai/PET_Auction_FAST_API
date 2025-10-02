from datetime import timedelta, datetime
import jwt
from api_v1.auth.token_director import TokenDirector
from api_v1.users.schemas import UserPublic
from core.config import settings


class AuthService:
    def __init__(self):
        self.token_director = TokenDirector(self.create_jwt)

    def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = None,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        payload = {"type": token_type, **token_data}
        return self.encode_jwt(
            payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def encode_jwt(
        self,
        payload: dict,
        expire_minutes: int = None,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now()
        expire_minutes = expire_minutes or settings.auth_jwt.access_token_expire_minutes
        expire = now + (
            expire_timedelta if expire_timedelta else timedelta(minutes=expire_minutes)
        )
        to_encode.update(exp=expire, iat=now)
        return jwt.encode(
            to_encode,
            settings.auth_jwt.private_key_path.read_text(),
            algorithm=settings.auth_jwt.algorithm,
        )

    def create_access_token(self, user: UserPublic) -> str:
        return self.token_director.create_access_token(user)

    def create_refresh_token(self, user: UserPublic) -> str:
        return self.token_director.create_refresh_token(user)


auth_service = AuthService()

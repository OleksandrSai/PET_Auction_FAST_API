from datetime import timedelta
from api_v1.users.schema import UserPublic
from utils.enums import TokenType


class TokenBuilder:
    def __init__(self, jwt_creator: callable):
        self._jwt_creator = jwt_creator
        self._token_type: TokenType | None = None
        self._user: UserPublic | None = None
        self._expire_minutes: int | None = None
        self._expire_timedelta: timedelta | None = None

    def for_user(self, user: UserPublic) -> "TokenBuilder":
        self._user = user
        return self

    def with_type(self, token_type: TokenType) -> "TokenBuilder":
        self._token_type = token_type
        return self

    def with_expire_minutes(self, minutes: int) -> "TokenBuilder":
        self._expire_minutes = minutes
        return self

    def with_expire_days(self, days: int) -> "TokenBuilder":
        self._expire_timedelta = timedelta(days=days)
        return self

    def build(self) -> str:
        if not self._token_type or not self._user:
            raise ValueError("Token type and user must be set")

        return self._jwt_creator(
            token_type=self._token_type,
            token_data=self._create_payload(),
            expire_minutes=self._expire_minutes,
            expire_timedelta=self._expire_timedelta,
        )

    def _create_payload(self) -> dict:
        return {
            "sub": self._user.id,
            "login": self._user.login,
            **(
                {"username": self._user.name}
                if self._token_type == TokenType.ACCESS
                else {}
            ),
        }

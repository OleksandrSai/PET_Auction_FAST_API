from api_v1.auth.token_builder import TokenBuilder
from api_v1.users.schema import UserPublic
from core.config import settings
from utils.enums import TokenType


class TokenDirector:

    def __init__(self, jwt_creator: callable):
        self._jwt_creator = jwt_creator

    def create_access_token(self, user: UserPublic) -> str:
        return (
            TokenBuilder(self._jwt_creator)
            .for_user(user)
            .with_type(TokenType.ACCESS)
            .with_expire_minutes(settings.auth_jwt.access_token_expire_minutes)
            .build()
        )

    def create_refresh_token(self, user: UserPublic) -> str:
        return (
            TokenBuilder(self._jwt_creator)
            .for_user(user)
            .with_type(TokenType.REFRESH)
            .with_expire_days(settings.auth_jwt.refresh_token_expire_days)
            .build()
        )

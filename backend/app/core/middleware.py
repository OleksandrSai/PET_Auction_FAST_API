from fastapi import Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError
from api_v1.auth.token_auth import auth_service
from core import db_helper
from core.config import settings
from utils.enums import TokenType
from api_v1.users.service import get_user


class AuthMiddleware(BaseHTTPMiddleware):
    msg_error = "Authorization header missing or invalid"

    def __init__(self, app):
        super().__init__(app)
        self.security = HTTPBearer(auto_error=False)
        self.excluded_paths = (
            f"{settings.api_v1_prefix}/auth/login",
            f"{settings.api_v1_prefix}/docs",
            f"{settings.api_v1_prefix}/redoc/",
            f"/openapi.json",
        )

    def is_excluded_path(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.excluded_paths)

    async def validate_access_token(self, token: str) -> bool:
        try:
            payload = auth_service.decode_jwt(token)
            return payload.get("type") == TokenType.ACCESS
        except ExpiredSignatureError:
            return False
        except InvalidTokenError:
            return False

    async def validate_refresh_token(self, token: str) -> dict | None:
        try:
            payload = auth_service.decode_jwt(token)
            if payload.get("type") == TokenType.REFRESH:
                return payload
            return None
        except (InvalidTokenError, ExpiredSignatureError):
            return None

    async def dispatch(self, request: Request, call_next):
        if self.is_excluded_path(request.url.path):
            return await call_next(request)

        credentials = await self.security(request)

        if credentials is None or credentials.scheme.lower() != "bearer":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": self.msg_error},
            )

        if await self.validate_access_token(credentials.credentials):
            return await call_next(request)

        refresh_payload = await self.validate_refresh_token(credentials.credentials)
        if refresh_payload:
            new_access_token = auth_service.create_refresh_token(
                user=get_user(
                    user_id=int(refresh_payload.get("sub")),
                    session=Depends(db_helper.scoped_session_dependency),
                )
            )
            response = await call_next(request)
            response.headers["X-New-Access-Token"] = new_access_token
            return response

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": self.msg_error},
        )

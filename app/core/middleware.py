from fastapi import Request, status
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse

from utils.security import decode_jwt
from core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
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

    async def validate_credentials(
        self, credentials: HTTPAuthorizationCredentials | None
    ) -> bool:
        try:
            if credentials is None or credentials.scheme.lower() != "bearer":
                return False
            decode_jwt(credentials.credentials)
            return True
        except InvalidTokenError:
            return False

    async def dispatch(self, request: Request, call_next):
        if self.is_excluded_path(request.url.path):
            return await call_next(request)

        credentials = await self.security(request)

        if not await self.validate_credentials(credentials):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing or invalid"},
            )

        return await call_next(request)

from fastapi import APIRouter, Depends
from . import schema
from .service import validate_user, refresher_token
from ..users.schema import UserPublic
from .token_auth import auth_service

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=schema.TokenInfo)
def auth_login(user: UserPublic = Depends(validate_user)):
    access_token = auth_service.create_access_token(user=user)
    refresh_token = auth_service.create_refresh_token(user=user)

    return schema.TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh/", response_model=schema.TokenInfo)
def refresh_access_token(user: UserPublic = Depends(refresher_token)):
    access_token = auth_service.create_access_token(user=user)
    return schema.TokenInfo(
        access_token=access_token,
    )

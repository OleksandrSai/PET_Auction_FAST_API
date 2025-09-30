from fastapi import APIRouter, Depends
from . import service
from . import schema
from ..users.schemas import UserPublic

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=schema.TokenInfo)
def auth_login(user: UserPublic = Depends(service.validate_user)):
    jwt_payload = {
        "sub": user.id,
        "username": user.name,
        "login": user.login,
    }
    token = service.encode_jwt(payload=jwt_payload)
    return schema.TokenInfo(access_token=token, token_type="Bearer")

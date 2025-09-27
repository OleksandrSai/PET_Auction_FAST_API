from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import db_helper

from . import crud
from .schemas import User, UserCreate

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_users(session=session)


@router.post("/", response_model=User)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await crud.get_user(user_id=user_id, session=session)
    if user is not None:
        return user

    raise HTTPException(status_code=404, detail="User not found")

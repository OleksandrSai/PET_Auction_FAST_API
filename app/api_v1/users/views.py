from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core import db_helper
from .dependencies import get_user_by_id
from . import service
from .schema import UserPublic, UserCreate, UserUpdate, UserUpdatePartial

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserPublic])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await service.get_users(session=session)


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.create_user(session=session, user_in=user_in)


@router.get("/{user_id}/", response_model=UserPublic)
async def get_user(
    user: UserPublic = Depends(get_user_by_id),
):
    return user


@router.put("/{user_id}/", response_model=UserPublic)
async def update_user(
    user_update: UserUpdate,
    user: UserPublic = Depends(get_user_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
):
    return await service.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/{user_id}/", response_model=UserPublic)
async def update_partial_user(
    user_update: UserUpdatePartial,
    user: UserPublic = Depends(get_user_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
):
    return await service.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


@router.delete(
    "/{user_id}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: UserPublic = Depends(get_user_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
) -> None:
    await service.delete_user(user_id=user.id, session=session)

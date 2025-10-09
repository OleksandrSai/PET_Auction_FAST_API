from typing import Annotated
from fastapi import Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from core import db_helper
from . import service


async def get_user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user: User = await service.get_user(user_id=user_id, session=session)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found",
    )

from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schemas import UserCreate
from core.models import User
from sqlalchemy.engine import Result
from sqlalchemy import select


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User | None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

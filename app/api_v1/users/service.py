from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schema import UserCreate, UserUpdate, UserUpdatePartial, UserPublic
from utils.security import hash_password
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
    hashed_password = hash_password(user_in.password)
    user_data = user_in.model_dump()
    user_data["password"] = hashed_password
    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: UserPublic,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> UserPublic:
    for key, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(
    user_id: int,
    session: AsyncSession,
) -> None:
    user = await session.get(User, user_id)
    await session.delete(user)
    await session.commit()

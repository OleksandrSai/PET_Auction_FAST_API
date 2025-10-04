import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users import service as user_service
from api_v1.users.schema import UserCreate
from core.models import User
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.mark.anyio
async def test_create_user(session: AsyncSession):
    user_in = UserCreate(login="alex", password="222", name="Oleksandr")
    user = await user_service.create_user(session, user_in)

    result = await session.execute(select(User).where(User.id == user.id))
    fetched_user = result.scalar_one()

    assert fetched_user.login == "alex"
    assert fetched_user.name == "Oleksandr"

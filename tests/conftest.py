import sys
import asyncio
import pytest
import asyncpg
from core.db_helper import DatabaseHelper
from core.models import Base
from core.config import settings

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

DATABASE_NAME = "test_db"
ADMIN_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:5432/postgres"
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:5432/{DATABASE_NAME}"

test_db_helper = DatabaseHelper(url=DATABASE_URL, echo=False)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def prepare_database():
    """Prepare database once per test session"""
    # Create database if not exists
    conn = await asyncpg.connect(ADMIN_URL)
    exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname=$1", DATABASE_NAME
    )
    if not exists:
        await conn.execute(f'CREATE DATABASE "{DATABASE_NAME}"')
    await conn.close()

    # Create tables
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Cleanup
    await test_db_helper.engine.dispose()


@pytest.fixture
async def session():
    """Database session fixture with rollback"""
    async with test_db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

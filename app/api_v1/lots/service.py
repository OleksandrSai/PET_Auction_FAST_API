from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result
from api_v1.lots.schema import CreateLot
from core.models import Lot


async def get_lots(session: AsyncSession) -> Sequence[Lot]:
    stmt = select(Lot).order_by(Lot.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_lot(session: AsyncSession, lot_in: CreateLot) -> Lot:
    lot = Lot(**lot_in.model_dump())
    session.add(lot)
    await session.commit()
    await session.refresh(lot)
    return lot

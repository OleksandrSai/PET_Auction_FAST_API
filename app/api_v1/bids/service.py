from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Bid
from sqlalchemy import Result
from . import schema


async def get_all_bids(session: AsyncSession) -> Sequence[Bid]:
    stmt = select(Bid).order_by(Bid.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_bid(session: AsyncSession, bid_in: schema.BidCreate) -> Bid:
    bid = Bid(**bid_in.model_dump())
    session.add(bid)
    await session.commit()
    await session.refresh(bid)
    return bid


async def delete_bid(session: AsyncSession, bid_id: int) -> None:
    bid = await session.get(Bid, bid_id)
    await session.delete(bid)
    await session.commit()

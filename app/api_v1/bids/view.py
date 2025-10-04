from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import db_helper
from . import service, schema

router = APIRouter(tags=["Bids"])


@router.get(path="/", response_model=schema.BaseBid)
async def get_bids(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await service.get_all_bids(session=session)


@router.post(path="/", response_model=schema.BidCreate)
async def get_bids(
    bid_in: schema.BidCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    return await service.create_bid(session=session, bid_in=bid_in)

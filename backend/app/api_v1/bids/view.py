from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core import db_helper
from . import service, schema

router = APIRouter(tags=["Bids"])


@router.get(path="/", response_model=List[schema.BidResponse])
async def get_bids(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await service.get_all_bids(session=session)


@router.post(path="/", response_model=schema.BidCreate)
async def get_bids(
    bid_in: schema.BidCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    return await service.create_bid(session=session, bid_in=bid_in)


@router.delete(path="/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def get_bids(
    bid_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    return await service.delete_bid(session=session, bid_id=bid_id)

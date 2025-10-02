from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import db_helper

router = APIRouter(tags=["Router"])


@router.get("/")
async def get_bids(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    pass

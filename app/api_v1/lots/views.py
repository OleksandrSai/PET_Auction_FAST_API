from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import schema
from . import service
from core import db_helper

router = APIRouter(tags=["Lots"])


@router.get(path="/", response_model=list[schema.BaseLot])
async def get_lots(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.get_lots(session=session)


@router.post(path="/", response_model=schema.CreateLot)
async def create_lot(
    lot_in: schema.CreateLot,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.create_lot(session=session, lot_in=lot_in)

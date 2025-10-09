from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from . import schema
from . import service
from core import db_helper

router = APIRouter(tags=["Lots"])


@router.get(path="/", response_model=list[schema.LotRelationShipsResponse])
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


@router.delete(path="/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_lot(
    lot_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    return await service.delete_lot(session=session, lot_id=lot_id)

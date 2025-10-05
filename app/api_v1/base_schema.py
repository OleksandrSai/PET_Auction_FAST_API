from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from utils.enums import BidState, LotState


class BaseOrmModel(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BaseUser(BaseOrmModel):
    login: str
    name: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class BaseLot(BaseOrmModel):
    title: str
    start_price: float
    state: LotState
    image_url: Optional[str]
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseBid(BaseOrmModel):
    amount: float
    state: BidState
    lot_id: int
    user_id: int
    created_at: datetime


BaseLot.model_rebuild()
BaseBid.model_rebuild()

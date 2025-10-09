from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from utils.enums import BidState, LotState


class BaseOrmModel(BaseModel):
  pass


class BaseUser(BaseOrmModel):
    login: str
    name: Optional[str]


class BaseLot(BaseOrmModel):
    title: str
    start_price: float
    state: LotState
    image_url: Optional[str]
    start_time: datetime
    end_time: datetime



class BaseBid(BaseOrmModel):
    amount: float
    state: BidState
    lot_id: int
    user_id: int


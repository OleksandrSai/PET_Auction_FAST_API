from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from api_v1.bids.schema import BaseBid
from utils.enums import LotState
from datetime import datetime, timezone


class BaseLot(BaseModel):
    title: str
    start_price: float
    state: LotState
    image_url: Optional[str]
    start_time: datetime
    end_time: datetime
    created_at: datetime

    @classmethod
    @field_validator("start_time", "end_time", "created_at")
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure datetime is timezone-aware and in UTC"""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        else:
            return v.astimezone(timezone.utc)


class CreateLot(BaseLot):
    pass


# class LotRelationshipModel(BaseLot):
#     bids: list[BaseBid]

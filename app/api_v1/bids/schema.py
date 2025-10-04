from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_validator
from utils.enums import BidState
from api_v1.users.schema import UserPublic


class BidCreate(BaseModel):
    amount: float
    state: BidState
    lot_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class BaseBid(BidCreate):
    created_at: datetime

    @classmethod
    @field_validator("created_at")
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure datetime is timezone-aware and in UTC"""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        else:
            return v.astimezone(timezone.utc)


class BidRelationshipModel(BaseBid):

    user: UserPublic

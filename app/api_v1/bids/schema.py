from __future__ import annotations
from datetime import datetime, timezone
from pydantic import field_validator, ConfigDict
from api_v1.base_schema import BaseBid, BaseLot, BaseUser
from api_v1.users.schema import UserPublic


class BidResponse(BaseBid):
    created_at: datetime
    user: UserPublic
    model_config = ConfigDict(from_attributes=True)


class BidCreate(BidResponse):
    @classmethod
    @field_validator("created_at")
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

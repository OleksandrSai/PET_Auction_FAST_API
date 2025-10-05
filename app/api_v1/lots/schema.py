from __future__ import annotations
from pydantic import field_validator, ConfigDict
from datetime import datetime, timezone
from api_v1.base_schema import BaseLot
from api_v1.bids.schema import BidResponse


class LotRelationShipsResponse(BaseLot):
    bids: list[BidResponse]
    max_bid: int | None
    model_config = ConfigDict(from_attributes=True)


class CreateLot(BaseLot):
    @classmethod
    @field_validator("start_time", "end_time", "created_at")
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure datetime is timezone-aware and in UTC"""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        else:
            return v.astimezone(timezone.utc)

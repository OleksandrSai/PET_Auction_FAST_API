from pydantic import field_validator, ConfigDict, field_serializer
from datetime import datetime, timezone
from api_v1.base_schema import BaseLot
from api_v1.bids.schema import BidResponse

from utils.enums import LotState


class LotRelationShipsResponse(BaseLot):
    id: int
    bids: list[BidResponse]
    max_bid: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

    @field_serializer('state')
    def serialize_state(self, state: LotState, _info):
        return state.name


class CreateLot(BaseLot):
    @classmethod
    @field_validator("start_time", "end_time", "created_at")
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure datetime is timezone-aware and in UTC"""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        else:
            return v.astimezone(timezone.utc)

from datetime import timezone, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from utils.enums import BidState
from .base import Base
from .user import User
from .lots import Lot


class Bid(Base):
    amount: Mapped[float] = mapped_column(default=0.0)
    state: Mapped[BidState] = mapped_column(default=BidState.PENDING)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lot.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    lot: Mapped["Lot"] = relationship("Lot", back_populates="bids")
    user: Mapped["User"] = relationship("User", back_populates="bids")

    def __repr__(self):
        return f"Bid({self.id=!r}, {self.state=!r}, {self.amount=!r}, {self.lot_id=!r}, {self.user_id=!r})"

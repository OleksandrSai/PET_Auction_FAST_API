from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base
from .user import User
from .lots import Lot


class Bid(Base):
    amount: Mapped[float] = mapped_column(default=0.0)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lot.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    lot: Mapped["Lot"] = relationship("Lot", back_populates="bids")
    user: Mapped["User"] = relationship("User", back_populates="bids")

    def __repr__(self):
        return f"Bid(id={self.id!r}, amount={self.amount!r}, lot_id={self.lot_id!r}, user_id={self.user_id!r})"

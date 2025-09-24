from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base
from .user import User
from .lots import Lot


class Bid(Base):
    lot_id: Mapped[int] = mapped_column(String(120))
    start_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="bids")
    lot: Mapped["Lot"] = relationship(back_populates="lot")

    def __repr__(self) -> str:
        return f"Bid(lot_id={self.id!r}, start_price={self.start_price!r}, is_active={self.is_active!r})"

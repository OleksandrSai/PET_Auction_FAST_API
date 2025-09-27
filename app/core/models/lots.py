from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base
from typing import List
from utils.enums import BidState


class Lot(Base):
    title: Mapped[str] = mapped_column(String(120))
    start_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    bid_state: Mapped[BidState] = mapped_column(default=BidState.running)

    bids: Mapped[List["Bid"]] = relationship(
        "Bid", back_populates="lot", cascade="all, delete-orphan", single_parent=True
    )

    def __repr__(self):
        return f"Lot(id={self.id!r}, title={self.title!r}, start_price={self.start_price!r}, bid_state={self.bid_state!r})"

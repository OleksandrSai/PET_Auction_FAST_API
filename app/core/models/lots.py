from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from .base import Base
from typing import List
from utils.enums import LotState
from datetime import timezone, datetime


class Lot(Base):
    title: Mapped[str] = mapped_column(String(120))
    start_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    state: Mapped[LotState] = mapped_column(default=LotState.SCHEDULED)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    bids: Mapped[List["Bid"]] = relationship(
        "Bid", back_populates="lot", cascade="all, delete-orphan", single_parent=True
    )

    def __repr__(self):
        return f"Lot({self.id=!r}, {self.title=!r}, {self.state=!r}, {self.start_price=!r} {self.image_url=!r})"

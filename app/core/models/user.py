from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import String
from .base import Base
from .bids import Bid


class User(Base):
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    bids: Mapped[List["Bid"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

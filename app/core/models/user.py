from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import String
from .base import Base


class User(Base):
    login: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    name: Mapped[Optional[str]] = mapped_column(default="Alex")
    balance: Mapped[float] = mapped_column(default=80000.0, nullable=False)

    bids: Mapped[List["Bid"]] = relationship(
        "Bid",
        back_populates="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self) -> str:
        return f"User({self.id=!r}, {self.login=!r}, {self.name=!r})"

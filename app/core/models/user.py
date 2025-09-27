from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import String
from .base import Base


class User(Base):
    login: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    name: Mapped[Optional[str]]

    bids: Mapped[List["Bid"]] = relationship(
        "Bid",
        back_populates="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, name={self.name!r})"

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

from enum import Enum, StrEnum, auto


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class LotState(Enum):
    RUNNING = auto()
    ENDED = auto()
    ARCHIVED = auto()
    SCHEDULED = auto()
    CANCELLED = auto()


class BidState(Enum):
    PENDING = auto()
    ACCEPTED = auto()
    REJECTED = auto()

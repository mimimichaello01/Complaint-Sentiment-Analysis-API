from infra.db.base import Base

from datetime import datetime

from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

from sqlalchemy import DateTime
from sqlalchemy import String

from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import Text


class Status(str, PyEnum):
    OPEN = "Open"
    CLOSED = "Closed"


class Sentiment(str, PyEnum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    UNKNOWN = "Unknown"


class Category(str, PyEnum):
    TECHNICAL = "Technical"
    PAYMENT = "Payment"
    OTHER = "Other"


class Complaint(Base):
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status), default=Status.OPEN, nullable=False
    )
    sentiment: Mapped[Sentiment] = mapped_column(SQLEnum(Sentiment), nullable=True)
    category: Mapped[Category] = mapped_column(
        SQLEnum(Category), default=Category.OTHER, nullable=True
    )

    ip: Mapped[str] = mapped_column(String(45), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    region: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

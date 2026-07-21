from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    venue: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    event_datetime: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
    )

    ticket_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    seats_available: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
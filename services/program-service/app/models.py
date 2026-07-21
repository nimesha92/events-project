from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    event_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    day: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    track: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    session_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    speaker_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    room: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
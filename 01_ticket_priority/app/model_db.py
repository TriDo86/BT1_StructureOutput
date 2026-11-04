from .database import Base

from sqlalchemy import Date, DateTime, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Email(Base):
    __tablename__ = "email"

    id: Mapped[str] = mapped_column(primary_key=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    message: Mapped[str] = mapped_column(Text)

class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[str] = mapped_column(primary_key=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    intent: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(10))
    product: Mapped[str] = mapped_column(String(100))
    summary: Mapped[str] = mapped_column(Text)
    needs_human_review: Mapped[bool] = mapped_column(Boolean)
from .database import Base

from sqlalchemy import Date, DateTime, String, Text, Boolean, ForeignKey
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

    id: Mapped[str] = mapped_column(ForeignKey("email.id"), primary_key=True) # Trace back Original Email, get received_at there
    intent: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(10))
    product: Mapped[str | None] = mapped_column(String(100), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    needs_human_review: Mapped[bool] = mapped_column(Boolean)


class TicketConfirmed(Base):
    __tablename__ = "ticket_confirmed"

    id: Mapped[str] = mapped_column(ForeignKey("ticket.id"), primary_key=True)
    intent: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(10))
    product: Mapped[str | None] = mapped_column(String(100), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    needs_human_review: Mapped[bool] = mapped_column(Boolean)

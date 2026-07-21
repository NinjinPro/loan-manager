from sqlalchemy import ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import Optional
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))  # in Rwf
    interest_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))  # percentage
    interest_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    total_due: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    is_paid: Mapped[bool] = mapped_column(default=False)
    due_date: Mapped[Optional[datetime]]
    paid_date: Mapped[Optional[datetime]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="transactions")
    person: Mapped["Person"] = relationship(back_populates="transactions")
from sqlalchemy import ForeignKey, Numeric, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import Optional
from datetime import datetime
import enum

class MoneyDirection(enum.Enum):
    MONEY_OUT = "money_out"   # You paid this person (you owe them)
    MONEY_IN  = "money_in"    # They paid you (they owe you)

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    direction: Mapped[MoneyDirection] = mapped_column(Enum(MoneyDirection), default=MoneyDirection.MONEY_OUT)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    interest_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    interest_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    total_due: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    is_paid: Mapped[bool] = mapped_column(default=False)
    due_date: Mapped[Optional[datetime]]
    paid_date: Mapped[Optional[datetime]]
    made_on: Mapped[Optional[datetime]]                # when the transaction actually happened
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())   # when it was recorded
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="transactions")
    person: Mapped["Person"] = relationship(back_populates="transactions")
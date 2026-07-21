from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import List, Optional
import enum

class PersonType(enum.Enum):
    CREDITOR = "creditor"   # user owes money to this person
    DEBTOR   = "debtor"     # this person owes money to user

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    phone: Mapped[Optional[str]]
    type: Mapped[PersonType] = mapped_column(Enum(PersonType))
    notes: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="people")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="person")
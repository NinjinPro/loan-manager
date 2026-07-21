from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import Optional, List

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    phone: Mapped[Optional[str]]
    notes: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="people")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="person")
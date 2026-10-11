from sqlalchemy import ForeignKey, Numeric, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from flask_login import UserMixin
from datetime import datetime
import enum
# from werkzeug.security import generate_password_hash, check_password_hash
from passlib.context import CryptContext
from database.main import Base

pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto'
)

class NotificationType(enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class MoneyDirection(enum.Enum):
    MONEY_OUT = "money_out"   # You paid this person (you owe them)
    MONEY_IN  = "money_in"    # They paid you (they owe you)

class Person(Base):
    __tablename__ = "people"

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    phone: Mapped[Optional[str]]
    notes: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="people")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="person")

    def to_dict(self, exclude:set|None=None):
        
        exclude = (exclude or set()).union([
            'user',
            'transactions',
        ])
        
        return super().to_dict(exclude)

class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType), default=NotificationType.INFO)
    is_read: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="notifications")

    def to_dict(self, exclude:set|None=None):
        
        exclude = (exclude or set()).union([
            'user',
        ])
        
        return super().to_dict(exclude)

class Transaction(Base):
    __tablename__ = "transactions"

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[str] = mapped_column(ForeignKey("people.id"))
    direction: Mapped[MoneyDirection] = mapped_column(Enum(MoneyDirection), default=MoneyDirection.MONEY_OUT)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    interest_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    interest_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    total_due: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    is_paid: Mapped[bool] = mapped_column(default=False)
    due_date: Mapped[Optional[datetime]]
    paid_date: Mapped[Optional[datetime]]
    made_on: Mapped[Optional[datetime]]         # when the transaction actually happened
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="transactions")
    person: Mapped["Person"] = relationship(back_populates="transactions")

    def to_dict(self, exclude:set|None=None):
        
        exclude = (exclude or set()).union([
            'user',
            'person',
        ])
        
        return super().to_dict(exclude)

class User(UserMixin, Base):
    __tablename__ = "users"

    # id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    main_color: Mapped[str] = mapped_column(default="#198754")  # Bootstrap green

    # relationships
    people: Mapped[List["Person"]] = relationship(back_populates="user", lazy="selectin")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user", lazy="selectin")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user", lazy="selectin")

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
        
    def to_dict(self, exclude:set|None=None):
        
        exclude = (exclude or set()).union([
            'people',
            'transaction',
            'notifications',
            'password_hash'
        ])
        
        return super().to_dict(exclude)


from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from db.database import Base
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

def generate_password_hash(v):
    return v

def check_password_hash(v1, v2):
    return v1 == v2
    
class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    main_color: Mapped[str] = mapped_column(default="#198754")  # Bootstrap green

    # relationships
    people: Mapped[List["Person"]] = relationship(back_populates="user")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
        
    def format(self):
        return {
            "username": self.username,
            " email": self.email
        }
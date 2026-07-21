from sqlalchemy import ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
import enum
from datetime import datetime

class NotificationType(enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str]
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType), default=NotificationType.INFO)
    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="notifications")
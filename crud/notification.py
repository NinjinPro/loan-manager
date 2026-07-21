# crud/notification_crud.py
from crud.base import BaseCRUD
from models.notification import Notification
from db.database import db
from sqlalchemy import select, desc
from typing import List

class NotificationCRUD(BaseCRUD[Notification]):
    def __init__(self):
        super().__init__(Notification)

    def get_unread(self, user_id: int) -> List[Notification]:
        return db.session.scalars(
            select(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .order_by(desc(Notification.created_at))
        ).all()

    def mark_as_read(self, notification_id: int):
        notif = self.get(notification_id)
        if notif:
            notif.is_read = True
            db.session.commit()
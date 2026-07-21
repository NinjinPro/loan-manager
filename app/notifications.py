# app/notifications.py
from db.database import db_session
from models.notification import Notification, NotificationType

def push_notification(user_id: int, message: str, ntype: str = "info"):
    """Create a persistent in-app notification for a user."""
    try:
        n_type = NotificationType(ntype)
    except ValueError:
        n_type = NotificationType.INFO
    
    notif = Notification(
        user_id=user_id,
        message=message,
        type=n_type
    )
    
    db_session.add(notif)
    db_session.commit()
    return notif
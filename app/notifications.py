from db.database import db
from models.notification import Notification, NotificationType

def push_notification(user_id: int, message: str, ntype: str = "info"):
    try:
        n_type = NotificationType(ntype)
    except ValueError:
        n_type = NotificationType.INFO
    notif = Notification(
        user_id=user_id,
        message=message,
        type=n_type
    )
    db.session.add(notif)
    db.session.commit()
    return notif
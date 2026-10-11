from database.main import db
from database.models import Notification, NotificationType

def push_notification(
    user_id: int,
    message: str,
    ntype: str = "info"
):
    try: 
        n_type = NotificationType(ntype)
    
    except ValueError:
        n_type = NotificationType.INFO
    
    notification = Notification(
        user_id=user_id,
        message=message,
        type=n_type
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return notification
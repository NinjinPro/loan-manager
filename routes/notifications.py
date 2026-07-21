# routes/notifications_api.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from crud.notification import NotificationCRUD

notif_api = Blueprint("notifications_api", __name__, url_prefix="/api/notifications")
notif_crud = NotificationCRUD()

@notif_api.route("/unread")
@login_required
def unread_notifications():
    notifs = notif_crud.get_unread(current_user.id)
    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "type": n.type.value,
            "created_at": n.created_at.isoformat()
        } for n in notifs
    ])

@notif_api.route("/<int:id>/read", methods=["POST"])
@login_required
def mark_read(id):
    notif_crud.mark_as_read(id)
    return jsonify(success=True)
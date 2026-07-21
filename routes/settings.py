# routes/settings.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.theme import generate_shades
from crud.user import UserCRUD

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")
user_crud = UserCRUD()

@settings_bp.route("/", methods=["GET", "POST"])
@login_required
def theme():
    if request.method == "POST":
        new_color = request.form["main_color"]
        if not new_color.startswith("#") or len(new_color) != 7:
            flash("Invalid colour code. Use #RRGGBB", "danger")
        else:
            user_crud.update(current_user.id, main_color=new_color)
            flash("Theme colour updated.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("settings.html", current_color=current_user.main_color)
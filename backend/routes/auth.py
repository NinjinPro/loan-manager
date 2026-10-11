# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from crud.user import UserCRUD

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
user_crud = UserCRUD()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_crud.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if user_crud.get_by_username(username):
            flash("Username already exists", "danger")
            return render_template("auth/register.html")

        # Create user with hashed password using user_crud method
        user = user_crud.create_user(username=username, email=email, password=password)
        login_user(user)
        flash("Account created!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
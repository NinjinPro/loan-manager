from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from crud.person import PersonCRUD
from crud.transaction import TransactionCRUD

people_bp = Blueprint("people", __name__, url_prefix="/people")
person_crud = PersonCRUD()
transaction_crud = TransactionCRUD()

@people_bp.route("/")
@login_required
def list_people():
    people = person_crud.get_by_user(current_user.id)
    for p in people:
        p.balance = transaction_crud.get_person_balance(p.id)
    return render_template("people/list.html", people=people)

@people_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_person():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form.get("phone")
        notes = request.form.get("notes")
        person_crud.create(
            user_id=current_user.id,
            name=name,
            phone=phone,
            notes=notes
        )
        flash(f"Person '{name}' added.", "success")
        return redirect(url_for("people.list_people"))
    return render_template("people/form.html", person=None)

@people_bp.route("/<int:id>")
@login_required
def person_detail(id):
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        flash("Person not found.", "danger")
        return redirect(url_for("people.list_people"))
    balance = transaction_crud.get_person_balance(person.id)
    transactions = transaction_crud.filter_by(person_id=person.id, user_id=current_user.id)
    return render_template(
        "people/detail.html",
        person=person,
        balance=balance,
        transactions=transactions
    )

@people_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_person(id):
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        flash("Person not found.", "danger")
        return redirect(url_for("people.list_people"))
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form.get("phone")
        notes = request.form.get("notes")
        person_crud.update(id, name=name, phone=phone, notes=notes)
        flash(f"'{name}' updated.", "success")
        return redirect(url_for("people.list_people"))
    return render_template("people/form.html", person=person)

@people_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_person(id):
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        flash("Person not found.", "danger")
        return redirect(url_for("people.list_people"))
    person_crud.delete(id)
    flash("Person deleted.", "info")
    return redirect(url_for("people.list_people"))
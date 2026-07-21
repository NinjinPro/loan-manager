# routes/people.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from crud.person import PersonCRUD
from models.person import PersonType

people_bp = Blueprint("people", __name__, url_prefix="/people")
person_crud = PersonCRUD()

@people_bp.route("/")
@login_required
def list_people():
    creditors = person_crud.get_creditors(current_user.id)
    debtors = person_crud.get_debtors(current_user.id)
    return render_template("people/list.html", creditors=creditors, debtors=debtors)

@people_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_person():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form.get("phone")
        ptype = request.form["type"]
        notes = request.form.get("notes")
        person_crud.create(
            user_id=current_user.id,
            name=name,
            phone=phone,
            type=PersonType(ptype),
            notes=notes
        )
        flash(f"{ptype.capitalize()} '{name}' added.", "success")
        return redirect(url_for("people.list_people"))
    return render_template("people/form.html", person=None)

@people_bp.route("/<int:id>")
@login_required
def person_detail(id):
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        flash("Person not found.", "danger")
        return redirect(url_for("people.list_people"))

    # Get all transactions for this person
    from crud.transaction import TransactionCRUD
    transaction_crud = TransactionCRUD()
    transactions = transaction_crud.filter_by(person_id=person.id, user_id=current_user.id)

    # Compute totals
    total_pending = sum(t.total_due or 0 for t in transactions if not t.is_paid)
    total_paid = sum(t.total_due or 0 for t in transactions if t.is_paid)
    total_all = total_pending + total_paid

    return render_template(
        "people/detail.html",
        person=person,
        transactions=transactions,
        total_pending=total_pending,
        total_paid=total_paid,
        total_all=total_all
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
        ptype = request.form["type"]
        notes = request.form.get("notes")
        person_crud.update(
            id,
            name=name,
            phone=phone,
            type=PersonType(ptype),
            notes=notes
        )
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
# routes/transactions.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from crud.transaction import TransactionCRUD
from crud.person import PersonCRUD
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")
transaction_crud = TransactionCRUD()
person_crud = PersonCRUD()

@transactions_bp.route("/")
@login_required
def list_transactions():
    person_id = request.args.get("person_id", type=int)
    status = request.args.get("status", "all")

    if person_id:
        person = person_crud.get(person_id)
        if not person or person.user_id != current_user.id:
            flash("Person not found.", "danger")
            return redirect(url_for("transactions.list_transactions"))
        transactions = transaction_crud.filter_by(person_id=person_id)
    else:
        transactions = transaction_crud.filter_by(user_id=current_user.id)

    # Filter by status if needed
    if status == "paid":
        transactions = [t for t in transactions if t.is_paid]
    elif status == "pending":
        transactions = [t for t in transactions if not t.is_paid]

    # Get all user's people for the "person" filter dropdown (optional)
    # Not strictly necessary here but good to show.
    return render_template(
        "transactions/list.html",
        transactions=transactions,
        person=person if person_id else None,
        status=status,
    )

@transactions_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        person_id = int(request.form["person_id"])
        amount = float(request.form["amount"])
        interest_rate = request.form.get("interest_rate")
        interest_amount = request.form.get("interest_amount")
        total_due = float(request.form["total_due"])
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        is_paid = request.form.get("is_paid") == "on"

        # Parse due_date
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        transaction_crud.create(
            user_id=current_user.id,
            person_id=person_id,
            amount=amount,
            interest_rate=float(interest_rate) if interest_rate else None,
            interest_amount=float(interest_amount) if interest_amount else None,
            total_due=total_due,
            description=description,
            due_date=due_date,
            is_paid=is_paid,
        )
        flash("Transaction saved.", "success")
        return redirect(url_for("transactions.list_transactions"))
    people = person_crud.filter_by(user_id=current_user.id)
    return render_template("transactions/form.html", transaction=None, people=people)

@transactions_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(id):
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    if request.method == "POST":
        person_id = int(request.form["person_id"])
        amount = float(request.form["amount"])
        interest_rate = request.form.get("interest_rate")
        interest_amount = request.form.get("interest_amount")
        total_due = float(request.form["total_due"])
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        is_paid = request.form.get("is_paid") == "on"

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        transaction_crud.update(
            id,
            person_id=person_id,
            amount=amount,
            interest_rate=float(interest_rate) if interest_rate else None,
            interest_amount=float(interest_amount) if interest_amount else None,
            total_due=total_due,
            description=description,
            due_date=due_date,
            is_paid=is_paid,
        )
        flash("Transaction updated.", "success")
        return redirect(url_for("transactions.list_transactions"))
    people = person_crud.filter_by(user_id=current_user.id)
    return render_template("transactions/form.html", transaction=transaction, people=people)

@transactions_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_transaction(id):
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    transaction_crud.delete(id)
    flash("Transaction deleted.", "info")
    return redirect(url_for("transactions.list_transactions"))

@transactions_bp.route("/<int:id>/mark_paid")
@login_required
def mark_paid(id):
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    transaction_crud.mark_paid(id)
    flash("Transaction marked as paid.", "success")
    return redirect(url_for("transactions.list_transactions"))



@transactions_bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
def detail(id):
    """View and edit all fields of a single transaction."""
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))

    if request.method == "POST":
        # Update all fields
        person_id = int(request.form["person_id"])
        amount = float(request.form["amount"])
        interest_rate = request.form.get("interest_rate")
        interest_amount = request.form.get("interest_amount")
        total_due = float(request.form["total_due"])
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        created_at_str = request.form.get("created_at")
        paid_date_str = request.form.get("paid_date")
        is_paid = request.form.get("is_paid") == "on"

        # Parse dates
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
        created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M") if created_at_str else transaction.created_at
        paid_date = datetime.strptime(paid_date_str, "%Y-%m-%dT%H:%M") if paid_date_str else None

        transaction_crud.update(
            id,
            person_id=person_id,
            amount=amount,
            interest_rate=float(interest_rate) if interest_rate else None,
            interest_amount=float(interest_amount) if interest_amount else None,
            total_due=total_due,
            description=description,
            due_date=due_date,
            created_at=created_at,
            paid_date=paid_date,
            is_paid=is_paid,
        )
        flash("Transaction updated.", "success")
        return redirect(url_for("transactions.detail", id=id))

    # Prepare date strings for the form
    def format_datetime(dt):
        return dt.strftime("%Y-%m-%dT%H:%M") if dt else ""

    return render_template(
        "transactions/detail.html",
        transaction=transaction,
        format_datetime=format_datetime,
        people=person_crud.filter_by(user_id=current_user.id)
    )
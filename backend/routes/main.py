from flask import Blueprint, render_template
from flask_login import login_required, current_user
from crud.person import PersonCRUD
from crud.transaction import TransactionCRUD

main_bp = Blueprint("main", __name__)
person_crud = PersonCRUD()
transaction_crud = TransactionCRUD()

@main_bp.route("/")
@login_required
def dashboard():
    people = person_crud.get_by_user(current_user.id)
    total_owed_to_me = 0
    total_i_owe = 0
    for person in people:
        bal = transaction_crud.get_person_balance(person.id)
        total_owed_to_me += bal["they_owe"]
        total_i_owe += bal["you_owe"]

    recent_transactions = transaction_crud.get_recent_by_user(current_user.id, limit=5)

    summary = {
        "people_count": len(people),
        "total_owed_to_me": total_owed_to_me,
        "total_i_owe": total_i_owe,
    }

    return render_template(
        "dashboard.html",
        summary=summary,
        recent_transactions=recent_transactions
    )
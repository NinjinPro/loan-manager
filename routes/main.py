# routes/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from crud.person import PersonCRUD
from crud.transaction import TransactionCRUD
from models.person import PersonType

main_bp = Blueprint("main", __name__)
person_crud = PersonCRUD()
transaction_crud = TransactionCRUD()

@main_bp.route("/")
@login_required
def dashboard():
    # Summary calculations
    debtors = person_crud.filter_by(user_id=current_user.id, type=PersonType.DEBTOR)
    creditors = person_crud.filter_by(user_id=current_user.id, type=PersonType.CREDITOR)

    total_owed_to_me = sum(
        t.total_due or 0 for debtor in debtors
        for t in debtor.transactions if not t.is_paid
    )
    total_i_owe = sum(
        t.total_due or 0 for creditor in creditors
        for t in creditor.transactions if not t.is_paid
    )

    recent_transactions = transaction_crud.get_recent_by_user(current_user.id, limit=5)

    summary = {
        "debtor_count": len(debtors),
        "creditor_count": len(creditors),
        "total_owed_to_me": total_owed_to_me,
        "total_i_owe": total_i_owe,
    }

    return render_template(
        "dashboard.html",
        summary=summary,
        recent_transactions=recent_transactions
    )
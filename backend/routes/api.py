from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from crud.person import PersonCRUD
from crud.transaction import TransactionCRUD
from models.transaction import MoneyDirection
from datetime import datetime

api_bp = Blueprint("api", __name__, url_prefix="/api")

person_crud = PersonCRUD()
transaction_crud = TransactionCRUD()

# ---------- PEOPLE ----------
@api_bp.route("/people")
@login_required
def get_people():
    people = person_crud.get_by_user(current_user.id)
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "phone": p.phone,
            "notes": p.notes,
            "user_id": p.user_id
        } for p in people
    ])

@api_bp.route("/people", methods=["POST"])
@login_required
def create_person():
    data = request.get_json()
    person = person_crud.create(
        user_id=current_user.id,
        name=data["name"],
        phone=data.get("phone"),
        notes=data.get("notes")
    )
    return jsonify({"id": person.id}), 201

@api_bp.route("/people/<int:id>", methods=["PUT"])
@login_required
def update_person(id):
    data = request.get_json()
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        return jsonify({"error": "Not found"}), 404
    person_crud.update(id, **data)
    return jsonify({"success": True})

@api_bp.route("/people/<int:id>", methods=["DELETE"])
@login_required
def delete_person(id):
    person = person_crud.get(id)
    if not person or person.user_id != current_user.id:
        return jsonify({"error": "Not found"}), 404
    for t in person.transactions:
        transaction_crud.delete(t.id)
    person_crud.delete(id)
    return jsonify({"success": True})

# ---------- TRANSACTIONS ----------
@api_bp.route("/transactions")
@login_required
def get_transactions():
    transactions = transaction_crud.filter_by(user_id=current_user.id)
    return jsonify([
        {
            "id": t.id,
            "person_id": t.person_id,
            "direction": t.direction.value,
            "amount": t.amount,
            "interest_rate": t.interest_rate,
            "interest_amount": t.interest_amount,
            "total_due": t.total_due,
            "is_paid": t.is_paid,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "paid_date": t.paid_date.isoformat() if t.paid_date else None,
            "made_on": t.made_on.isoformat() if t.made_on else None,
            "created_at": t.created_at.isoformat(),
            "description": t.description,
            "user_id": t.user_id
        } for t in transactions
    ])

@api_bp.route("/transactions", methods=["POST"])
@login_required
def create_transaction():
    data = request.get_json()
    due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
    paid_date = datetime.fromisoformat(data["paid_date"]) if data.get("paid_date") else None
    made_on = datetime.fromisoformat(data["made_on"]) if data.get("made_on") else None
    created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow()

    t = transaction_crud.create(
        user_id=current_user.id,
        person_id=data["person_id"],
        direction=MoneyDirection(data["direction"]),
        amount=data["amount"],
        interest_rate=data.get("interest_rate"),
        interest_amount=data.get("interest_amount"),
        total_due=data["total_due"],
        is_paid=data.get("is_paid", False),
        due_date=due_date,
        paid_date=paid_date,
        made_on=made_on,
        created_at=created_at,
        description=data.get("description")
    )
    return jsonify({"id": t.id}), 201

@api_bp.route("/transactions/<int:id>", methods=["PUT"])
@login_required
def update_transaction(id):
    data = request.get_json()
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        return jsonify({"error": "Not found"}), 404

    update_data = {k: v for k, v in data.items() if k not in ("created_at", "due_date", "paid_date", "made_on")}
    if "due_date" in data and data["due_date"]:
        update_data["due_date"] = datetime.fromisoformat(data["due_date"])
    if "paid_date" in data and data["paid_date"]:
        update_data["paid_date"] = datetime.fromisoformat(data["paid_date"])
    if "made_on" in data and data["made_on"]:
        update_data["made_on"] = datetime.fromisoformat(data["made_on"])
    if "created_at" in data and data["created_at"]:
        update_data["created_at"] = datetime.fromisoformat(data["created_at"])
    if "direction" in data:
        update_data["direction"] = MoneyDirection(data["direction"])

    transaction_crud.update(id, **update_data)
    return jsonify({"success": True})

@api_bp.route("/transactions/<int:id>", methods=["DELETE"])
@login_required
def delete_transaction(id):
    transaction = transaction_crud.get(id)
    if not transaction or transaction.user_id != current_user.id:
        return jsonify({"error": "Not found"}), 404
    transaction_crud.delete(id)
    return jsonify({"success": True})
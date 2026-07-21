# crud/transaction_crud.py
from crud.base import BaseCRUD
from models.transaction import Transaction
from db.database import db
from sqlalchemy import select, desc
from datetime import datetime
from typing import List

class TransactionCRUD(BaseCRUD[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_recent_by_user(self, user_id: int, limit: int = 5) -> List[Transaction]:
        return db.session.scalars(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(desc(Transaction.created_at))
            .limit(limit)
        ).all()

    def mark_paid(self, transaction_id: int):
        trans = self.get(transaction_id)
        if trans and not trans.is_paid:
            trans.is_paid = True
            trans.paid_date = datetime.utcnow()
            db.session.commit()
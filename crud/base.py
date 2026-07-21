# crud/base.py
from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy import select, delete, update
from db.database import db

T = TypeVar("T")

class BaseCRUD(Generic[T]):
    """Generic CRUD for a SQLAlchemy model."""

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def get(self, obj_id: int) -> Optional[T]:
        return db.session.get(self.model, obj_id)

    def get_all(self) -> List[T]:
        return db.session.scalars(select(self.model)).all()

    def filter_by(self, **kwargs) -> List[T]:
        return db.session.scalars(select(self.model).filter_by(**kwargs)).all()

    def update(self, obj_id: int, **kwargs) -> Optional[T]:
        instance = self.get(obj_id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, obj_id: int) -> bool:
        instance = self.get(obj_id)
        if instance is None:
            return False
        db.session.delete(instance)
        db.session.commit()
        return True

    def paginate(self, page: int = 1, per_page: int = 20) -> dict:
        """Return a dict with items, total, etc. for pagination."""
        offset = (page - 1) * per_page
        items = db.session.scalars(
            select(self.model).limit(per_page).offset(offset)
        ).all()
        total = db.session.scalar(select(func.count()).select_from(self.model))
        return {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page if total else 0,
        }
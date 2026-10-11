from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy import select
from database.main import db

ModelType = TypeVar("ModelType")

class BaseCRUD(Generic[ModelType]):
    """Generic CRUD for a SQLAlchemy model."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        
        return instance

    def get(self, obj_id: int) -> Optional[ModelType]:
        return db.session.get(self.model, obj_id)

    def get_all(self) -> List[ModelType]:
        return db.session.scalars(select(self.model)).all()

    def filter_by(self, **kwargs) -> List[ModelType]:
        return db.session.scalars(select(self.model).filter_by(**kwargs)).all()

    def update(self, obj_id: int, **kwargs) -> Optional[ModelType]:
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

        query = select(self.model).limit(per_page).offset(offset)
        items = db.session.scalars(query).all()
        
        total = db.session.scalar(select(func.count()).select_from(self.model))

        pages = 0

        if total:
            pages = (total + per_page - 1) // per_page
        
        return {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
        }
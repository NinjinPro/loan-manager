# crud/user_crud.py
from crud.base import BaseCRUD
from models.user import User
from db.database import db
from typing import Optional
from sqlalchemy import select

class UserCRUD(BaseCRUD[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> Optional[User]:
        return db.session.scalars(
            select(User).where(User.username == username)
        ).first()

    def create_user(self, username: str, email: str, password: str) -> User:
        """Create a user with hashed password and commit."""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
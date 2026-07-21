from crud.base import BaseCRUD
from models.person import Person
from db.database import db
from sqlalchemy import select

class PersonCRUD(BaseCRUD[Person]):
    def __init__(self):
        super().__init__(Person)

    def get_by_user(self, user_id: int):
        return db.session.scalars(
            select(Person).where(Person.user_id == user_id)
        ).all()
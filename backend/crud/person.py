from crud.base import BaseCRUD
from database.main import db
from database.models import Person
from sqlalchemy import select

class PersonCRUD(BaseCRUD[Person]):
    def __init__(self):
        super().__init__(Person)

    def get_by_user(self, user_id: int):
        return db.session.scalars(
            select(Person).where(Person.user_id == user_id)
        ).all()
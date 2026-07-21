# crud/person_crud.py
from crud.base import BaseCRUD
from models.person import Person, PersonType

class PersonCRUD(BaseCRUD[Person]):
    def __init__(self):
        super().__init__(Person)

    def get_creditors(self, user_id: int):
        return self.filter_by(user_id=user_id, type=PersonType.CREDITOR)

    def get_debtors(self, user_id: int):
        return self.filter_by(user_id=user_id, type=PersonType.DEBTOR)
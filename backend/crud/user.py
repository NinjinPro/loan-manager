from crud.base import BaseCRUD
from database.main import db
from database.models import User
from typing import Optional
from sqlalchemy import select
import string

def isValidEmail(email: str):
    if '@' not in email:
        return False
    
    email, domain = email.split('@')
    if not email or not domain:
        return False

    if '.' not in domain:
        return False

    carrier, dot_com = domain.split('.')
    if not carrier or not dot_com:
        return False

    return True

def isPasswordStrong(password):
    if len(password.strip()) < 8:
        return False
    
    digits = set(string.digits)
    lowercase = set(string.ascii_lowercase)
    uppercase = set(string.ascii_uppercase)
    punctuation = set(string.punctuation)
    # password = set(password)

    return all([
        digits.intersection(password),
        lowercase.intersection(password),
        uppercase.intersection(password),
        punctuation.intersection(password),
    ])
    
class UserCRUD(BaseCRUD[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        return db.session.scalars(query).first()

    # @overload
    def create(self, username: str, email: str, password: str) -> User:
        """Create a user with hashed password and commit."""

        # verify username, email and password
        if self.get_by_username(username):
            raise ValueError('Username already taken')
        
        if not username:
            raise ValueError('Invalid username')

        if not isValidEmail(email):
            raise ValueError('Invalid email')
        
        if not isPasswordStrong(password):
            raise ValueError('Weak password')
        
        user = User(username=username, email=email)
        user.set_password(password)

        # save to database
        db.session.add(user)
        db.session.commit()
        
        return user
from flask import Flask
from app.config import Config

app = Flask("Testing...")
app.config.from_object(Config)

from db.database import db
from sqlalchemy import select

db.init_app(app)

from models.user import User
from models.transaction import Transaction
from models.person import Person
from models.notification import Notification

users = db.session.scalars(select(User)).all()
transactions = db.session.scalars(select(Transaction)).all()
persons = db.session.scalars(select(Person)).all()
notifications = db.session.scalars(select(Notification)).all()

for user in users:
    print("user", user)

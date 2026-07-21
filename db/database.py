# db/database.py

from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
    scoped_session,
)


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self._engine = None
        self._session_factory = None
        self._db_session = None

    def init_app(self, app: Flask):
        self._engine = create_engine(
            app.config["SQLALCHEMY_DATABASE_URI"],
            **(app.config.get("SQLALCHEMY_ENGINE_OPTIONS") or {})
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            future=True,
        )

        self._db_session = scoped_session(self._session_factory)

        @app.before_request
        def inject_session():
            g.db = self._db_session()

        @app.teardown_appcontext
        def remove_session(exception=None):
            self._db_session.remove()

    @property
    def engine(self):
        if self._engine is None:
            raise RuntimeError("Database has not been initialized.")
        return self._engine

    @property
    def session_factory(self):
        if self._session_factory is None:
            raise RuntimeError("Database has not been initialized.")
        return self._session_factory

    @property
    def session(self):
        if self._db_session is None:
            raise RuntimeError("Database has not been initialized.")
        return self._db_session

db = Database()

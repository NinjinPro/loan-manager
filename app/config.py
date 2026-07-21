# app/config.py
import os
from dotenv import loadenv

loadenv()

class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///loan_manager.db"
    )
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
                "pool_size": 10,
                "pool_recycle": 3600,
                "pool_pre_ping": True,
            }

    #def __post_init__(self):
        #if not self.SQLALCHEMY_ENGINE_OPTIONS:
            #self.SQLALCHEMY_ENGINE_OPTIONS = 
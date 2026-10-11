import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_DEV") if os.getenv("ENVIRONMENT") == "development" else os.getenv("DATABASE_URI_PROD")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }

ConfigInstance = Config()
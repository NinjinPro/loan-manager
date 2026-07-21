from flask import Flask, Blueprint

from .auth import auth_bp
from .person import people_bp
from .transactions import transactions_bp
from .settings import settings_bp
from .notifications import notif_api
from .main import main_bp
from .api import api_bp

__all__ = [
	api_bp,
    main_bp,
    notif_api,
    settings_bp,
    transactions_bp,
    people_bp,
    auth_bp,
]

def register_bps(app: Flask, bps: list[Blueprint] = __all__) -> None:
    for bp in bps:
        app.register_blueprint(bp)
        
#
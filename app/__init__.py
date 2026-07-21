# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from app.config import Config
from db.database import db, Base
from models import __all__

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(config_class=Config):
    app = Flask(
        "LOAN MANAGER APP",
        template_folder='./templates',
        static_folder='./static',
        static_url_path='/static',
    )
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from crud.user import UserCRUD
        return UserCRUD().get(int(user_id))

    # Create tables (dev only – use migrations in prod)
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)

    # Register blueprints
    from routes import register_bps
    register_bps(app)
    

    # Context processor for theme shades
    @app.context_processor
    def inject_theme():
        from flask_login import current_user
        from app.theme import generate_shades
        if current_user.is_authenticated:
            shades = generate_shades(current_user.main_color)
        else:
            shades = generate_shades("#198754")
        return dict(theme_shades=shades)
        
    @app.template_filter('rwf')
    def format_rwf(value):
        if value is None:
            return ""
        return f"{value:,.0f} Rwf"

    return app
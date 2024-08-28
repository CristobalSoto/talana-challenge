from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure all tables are created

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

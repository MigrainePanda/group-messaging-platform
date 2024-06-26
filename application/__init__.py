from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()
engine = create_engine("sqlite:///instance/project.db")

from application.routes.users import users_bp
from application.routes.chat import chat_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.register_blueprint(chat_bp)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

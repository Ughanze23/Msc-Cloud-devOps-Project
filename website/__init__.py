from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    """Create Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hash-session-data"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    
    #init database
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    #register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    #create database
    create_database(app)

    #create roles
    create_roles(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():  # Push the app context
            db.create_all()
            logging.info("Database created successfully")

def create_roles(app):
    """Insert roles into thecl Role table only if they don't already exist."""
    from .models import Role
    with app.app_context():
        roles = [
            {"id": 1, "role_name": "admin"},
            {"id": 2, "role_name": "editor"},
            {"id": 3, "role_name": "viewer"},
        ]
        
        for role_data in roles:
            # Check if role already exists
            role = Role.query.filter_by(role_name=role_data["role_name"]).first()
            
            if not role:
                # If role doesn't exist, create and add it to the session
                new_role = Role(id=role_data["id"], role_name=role_data["role_name"])
                db.session.add(new_role)
                logging.info(f"Role '{role_data['role_name']}' added successfully!")
            else:
                logging.info(f"Role '{role_data['role_name']}' already exists, skipping.")
        
        # Commit the session to save the new roles
        db.session.commit()

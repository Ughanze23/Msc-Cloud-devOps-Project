from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
import logging
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

db = SQLAlchemy()

def create_app():
    load_dotenv()
    """Create Flask app"""
    application = Flask(__name__)
    application.config["SECRET_KEY"] = "Hash-session-data"
    
    # Configure database URI based on environment
    if application.config.get("TESTING"):
        application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        DB_USER = os.environ.get("DB_USER", "postgres")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "K$K$rot2024")
        DB_HOST = os.environ.get("DB_HOST", "database-1.cvhifpi70v8r.us-east-1.rds.amazonaws.com")
        DB_NAME = os.environ.get("DB_NAME", "Cloud_DevOPsSec")
        application.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # Initialize database
    db.init_app(application)

    from .views import views
    from .auth import auth
    from .models import User, Glossary

    # Register blueprints
    application.register_blueprint(views, url_prefix="/")
    application.register_blueprint(auth, url_prefix="/")

    # Create database and initial data
    with application.app_context():
        db.create_all()
        logging.info("Database tables created successfully")
        
        if not application.config.get("TESTING"):
            try:
                create_roles(application)
                create_admin(application)
            except Exception as e:
                logging.error(f"Error during initialization: {str(e)}")


    # Configure login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return application


def create_roles(application):
    """Create roles if they don't exist"""
    from .models import Role

    with application.app_context():
        roles = [
            {"id": 1, "role_name": "admin"},
            {"id": 2, "role_name": "editor"},
            {"id": 3, "role_name": "viewer"},
        ]

        for role_data in roles:
            try:
                # Check if role exists 
                existing_role = Role.query.filter(
                    (Role.id == role_data["id"]) | 
                    (Role.role_name == role_data["role_name"])
                ).first()

                if not existing_role:
                    new_role = Role(id=role_data["id"], role_name=role_data["role_name"])
                    db.session.add(new_role)
                    db.session.commit()
                    logging.info(f"Role '{role_data['role_name']}' added successfully!")
                else:
                    if existing_role.id != role_data["id"]:
                        logging.warning(
                            f"Role '{role_data['role_name']}' exists with different id: {existing_role.id}"
                        )
                    else:
                        logging.info(f"Role '{role_data['role_name']}' already exists.")
                        
            except IntegrityError as e:
                db.session.rollback()
                logging.error(f"IntegrityError creating role {role_data['role_name']}: {str(e)}")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error creating role {role_data['role_name']}: {str(e)}")

def create_admin(application):
    """Create admin user if it doesn't exist"""
    from .models import User
    from werkzeug.security import generate_password_hash

    with application.app_context():
        try:
            user = User.query.filter_by(username="superadmin").first()

            if not user:
                admin = User(
                    email="admin@gmail.com",
                    username="superadmin",
                    password=generate_password_hash("admin", method="pbkdf2:sha256"),
                    role_id=1,
                )
                db.session.add(admin)
                db.session.commit()
                logging.info("Admin created successfully")
            else:
                logging.info("Admin user already exists")
                
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError creating admin user: {str(e)}")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating admin user: {str(e)}")
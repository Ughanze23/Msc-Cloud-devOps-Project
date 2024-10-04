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
    from .models import User,Role

    #register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    #create database
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    from .models import Role
    if not path.exists("website/" + DB_NAME):
        with app.app_context():  # Push the app context
            db.create_all()
            logging.info("Database created successfully")

        # Insert roles
            admin_role = Role(id=1, name='admin')
            editor_role = Role(id=2, name='editor')
            viewer_role = Role(id=3, name='viewer')

            db.session.add(admin_role)
            db.session.add(editor_role)
            db.session.add(viewer_role)

            db.session.commit()
            logging.info("Roles added successfully!")        
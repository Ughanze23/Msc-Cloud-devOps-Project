from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import views
from .auth import auth

def create_app():
    """Create Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hash-session-data"

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
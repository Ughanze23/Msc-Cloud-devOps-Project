from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



def create_app():
    """Create Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hash-session-data"

    return app
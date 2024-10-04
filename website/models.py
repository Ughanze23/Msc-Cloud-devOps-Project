from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    created_at =  db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(),onupdate=func.now())
    role_id  = db.Column(db.Integer, db.ForeignKey('role.id'),default=3)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False, unique=True)
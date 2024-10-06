from flask import Blueprint, render_template, request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Glossary, User
from . import db
import logging

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html",user=current_user)

@login_required
@views.route("/glossary",methods=["GET","PUT"])
def glossary():
    """View all busness glossary page"""
    glossaries = Glossary.query.all()
    return render_template("glossary.html",user=current_user, glossaries = glossaries)

@login_required
@views.route("/post-glossary", methods=["GET","POST"])
def post_glossary():
    """Post Glossary page"""
    if request.method == "POST":
        name = request.form.get("name").title()
        type = request.form.get("type")
        description = request.form.get("description").capitalize()

        if not name:
            flash("Enter a business term name", category="error")
        elif not type:
            flash("Select a type for the business term", category="error")
        elif not description:
            flash("", category="error")
        else :
            entry = Glossary(posted_by=current_user.id,name=name,type=type,description=description)
            db.session.add(entry)
            db.session.commit()
            flash("Entry Successful..", category="success")
            return redirect(url_for("views.glossary"))

    return render_template("post-glossary.html",user=current_user)

@login_required
@views.route("/users",methods=["GET","POST","PUT","DELETE"])
def users():
    """Admin Page"""
    users = User.query.all()
    return render_template("users.html",user=current_user,users=users)


@login_required
@views.route("/users/delete-user/<user_id>")
def delete_user(user_id):
    """delete user"""

    user = User.query.filter_by(id=user_id).first()

    if current_user.role.role_name == "admin":
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Successfully", category="success")
        return redirect(url_for("views.users"))

    else:
        flash("You are not authorized to perform this operation!", category="error")
    return redirect(url_for("views.users"))
from flask import Blueprint, render_template, request,flash
from flask_login import login_required,current_user
from .models import Glossary
from . import db


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
    return render_template("glossary.html",user=current_user)

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
            entry = Glossary(posted_by=current_user.id,name=name,type=type,description=description,)
            db.session.add(entry)
            db.session.commit()
            flash("Entry Successful..", category="success")

    return render_template("post-glossary.html",user=current_user)

@login_required
@views.route("/admin",methods=["GET","POST","PUT","DELETE"])
def admin():
    """Admin Page"""
    return render_template("admin.html",user=current_user)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Glossary, User
from . import db
import logging

views = Blueprint("views", __name__)

GLOSSARYPAGE = "views.glossary"
AUTH_ERR_MSG = "You are not authorized to perform this operation!"
USERSPAGE = "views.users"

# ----------------- homepage ------------------
@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)

# ---------------------- glossary page ------------------------------
@login_required
@views.route("/glossary", methods=["GET"])  
def glossary():
    """View all business glossary page"""
    glossaries = Glossary.query.all()
    return render_template("glossary.html", user=current_user, glossaries=glossaries)

@login_required
@views.route("/post-glossary", methods=["GET", "POST"])
def post_glossary():
    """Post Glossary page"""
    if request.method == "POST":
        name = request.form.get("name").title()
        category = request.form.get("category")
        description = request.form.get("description").capitalize()

        if not name:
            flash("Enter a business term name", category="error")
        elif not category: 
            flash("Select a type for the business term", category="error")
        elif not description:
            flash("Please enter a description for the business term", category="error")
        else:
            entry = Glossary(
                posted_by=current_user.id,
                name=name,
                type=category,
                description=description,
            )
            db.session.add(entry)
            db.session.commit()
            flash("Business Term Created Successfully..", category="success")
            return redirect(url_for(GLOSSARYPAGE))

    return render_template("post-glossary.html", user=current_user)

@login_required
@views.route("/glossary/edit-term/<int:entry_id>", methods=["GET", "POST"])
def edit_term(entry_id):
    """update Business term details"""
    entry = Glossary.query.filter_by(id=entry_id).first()
    
    if not entry:
        flash("Entry not found.", "error")
        return redirect(url_for(GLOSSARYPAGE))

    if request.method == "POST":
        new_business_category = request.form.get("category")
        new_description = request.form.get("description")

        if not new_business_category and not new_description:
            flash("Enter a new Category or Business term description.", "error")
            return redirect(url_for(GLOSSARYPAGE))

        if new_business_category:
            entry.type = new_business_category

        if new_description:
            entry.description = new_description

        db.session.commit()
        flash("Business term updated successfully", "success")
        return redirect(url_for(GLOSSARYPAGE))

    return render_template("glossary.html", user=current_user, entry=entry)

@login_required
@views.route("/glossary/delete-entry/<entry_id>", methods=["POST"])
def delete_entry(entry_id):
    """delete entry"""
    entry = Glossary.query.filter_by(id=entry_id).first()

    if not entry:
        flash("Entry not found.", "error")
        return redirect(url_for(GLOSSARYPAGE))

    if current_user.role.role_name == "admin":
        db.session.delete(entry)
        db.session.commit()
        flash("Entry Deleted Successfully", category="success")
        return redirect(url_for(GLOSSARYPAGE))
    else:
        flash(AUTH_ERR_MSG, category="error")
        return redirect(url_for(GLOSSARYPAGE))

# ------------------- users page ----------------------------
@login_required
@views.route("/users", methods=["GET"])  
def users():
    """Admin Page"""
    users = User.query.all()
    return render_template("users.html", user=current_user, users=users)

@login_required
@views.route("/users/delete-user/<user_id>", methods=["POST"])
def delete_user(user_id):
    """delete user"""
    user = User.query.filter_by(id=user_id).first()

    if not user:
        flash("User not found.", "error")
        return redirect(url_for(USERSPAGE))

    if current_user.role.role_name == "admin":
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Successfully", category="success")
        return redirect(url_for(USERSPAGE))
    else:
        flash(AUTH_ERR_MSG, category="error")
        return redirect(url_for(USERSPAGE))

@login_required
@views.route("/change-role/user_id=<int:user_id>", methods=["POST"])
def change_role(user_id):
    """change user role"""
    new_role = request.form.get("role", type=int)  # updated this from parsing args to using a form. (CSRF security best practice)
    user = User.query.filter_by(id=user_id).first()

    if not user:
        flash("User not found.", "error")
        return redirect(url_for(USERSPAGE))

    if current_user.role.role_name != "admin":
        flash(AUTH_ERR_MSG, category="error")
        return redirect(url_for(USERSPAGE))

    elif user.role_id == new_role:
        flash("The selected role is the same as the current role.", category="error")
        return redirect(url_for(USERSPAGE))

    else:
        user.role_id = new_role
        db.session.commit()
        flash("User role updated successfully", category="success")

    return redirect(url_for(USERSPAGE))
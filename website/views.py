from flask import Blueprint, render_template
from flask_login import login_required,current_user

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html",name=current_user.username)

@login_required
@views.route("/glossary")
def glossary():
    return render_template("glossary.html")

@login_required
@views.route("/post-glossary")
def post_glossary():
    return render_template("post-glossary.html")

@login_required
@views.route("/admin")
def admin():
    return render_template("admin.html",)
from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
def home():
    return render_template("home.html")

@views.route("/log-in")
def log_in():
    return render_template("log-in.html")

@views.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")

@views.route("/glossary")
def glossary():
    return render_template("glossary.html")

@views.route("/post-glossary")
def post_glossary():
    return render_template("post-glossary.html")

@views.route("/admin")
def admin():
    return render_template("admin.html")
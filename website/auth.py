from flask import Blueprint, render_template,redirect,url_for

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("log-in.html")

@auth.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")

@auth.route("/log-out")
def log_out():
    return redirect(url_for("views.log_in"))
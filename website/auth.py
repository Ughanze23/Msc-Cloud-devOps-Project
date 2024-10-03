from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "home"

@auth.route("/sign-up")
def sign_up():
    return "home"

@auth.route("/log-out")
def log_out():
    return ""
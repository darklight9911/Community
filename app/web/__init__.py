from flask import Blueprint, render_template, redirect, url_for

web_bp = Blueprint("web", __name__)

@web_bp.get("/")
def landing():
    return render_template("index.html")

@web_bp.get("/login")
def login_page():
    return render_template("login.html")

@web_bp.get("/signup")
def signup_page():
    return render_template("signup.html")

@web_bp.get("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

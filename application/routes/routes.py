from flask import render_template, request, redirect, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.extensions import mongo
from application.routes.forms import RegistrationForm, LoginForm


main = Blueprint('main', __name__)

@main.route("/")
def home():
    docs = mongo.db.test.find()
    return render_template("home.html", docs = docs)

@main.route("/admin")
def admin():
    pass

@main.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title = "Register", form = form)

@main.route("/login")
def login():
    form = LoginForm()
    return render_template("Login.html", title = "Login", form = form)
from flask import render_template, request, redirect, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.extensions import mongo
from application.routes.forms import RegistrationForm, LoginForm


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    docs = mongo.db.test.find()
    return render_template("home.html", title = "Home",  docs = docs)


@main.route("/about")
def about():

    return render_template("about.html", title = "About")

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
    return render_template("login.html", title = "Login", form = form)

@main.route("/sidebar")
def sidebar():
    return render_template("sidebar.html")
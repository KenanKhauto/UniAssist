from flask import render_template, request, redirect, Blueprint, flash, url_for
from application import login_manager, bcrypt
from application.routes.forms import RegistrationForm, LoginForm
from application.custom import user_rep

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return user_rep.find_user_by_id(user_id)

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html", title = "Home")


@main.route("/about")
def about():

    return render_template("about.html", title = "About")

@main.route("/admin")
def admin():
    pass


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_rep.register_user(username=form.username.data, password=hashed_password, email=form.email.data)
        flash(f"Your account has been created! You are now able to log in", category="success")
        return redirect(url_for("main.login"))
    return render_template("register.html", title = "Register", form = form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title = "Login", form = form)
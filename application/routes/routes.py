import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app
from application import login_manager, bcrypt
from application.routes.forms import RegistrationForm, LoginForm, UpdateAccountForm
from application.custom import user_rep
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    """
    Callback function for Flask-Login to load a user from user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object associated with the user ID.
    """
    return user_rep.find_user_by_id(user_id)


@main.route("/")
@main.route("/home")
def home():
    """
    Route handler for the home page.

    Returns:
        str: Rendered template for the home page.
    """
    return render_template("home.html", title="Home")


@main.route("/about")
def about():
    """
    Route handler for the about page.

    Returns:
        str: Rendered template for the about page.
    """
    return render_template("about.html", title="About")


@main.route("/admin")
def admin():
    """
    Route handler for the admin page.

    Returns:
        None
    """
    pass


@main.route("/register", methods=["GET", "POST"])
def register():
    """
    Route handler for user registration.

    If the user is already authenticated, they are redirected to the home page.
    If the registration form is submitted and valid, the user is registered, a success message 
    is flashed, and they are redirected to the login page.

    Returns:
        str: Rendered template for the registration page or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_rep.register_user(username=form.username.data, password=hashed_password, email=form.email.data)
        flash(f"Your account has been created! You are now able to log in", category="success")
        return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    Route handler for user login.

    If the user is already authenticated, they are redirected to the home page.
    If the login form is submitted and valid, the user is logged in, a success message is flashed, 
    and they are redirected to the home page.

    Returns:
        str: Rendered template for the login page or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    return render_template("login.html", title = "Login", form = form)
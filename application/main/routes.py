

from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app


main = Blueprint('main', __name__)


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

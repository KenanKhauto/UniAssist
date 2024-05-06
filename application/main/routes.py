

from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app
from application.custom import user_rep, post_rep
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    """
    Route handler for the home page.

    Returns:
        str: Rendered template for the home page.
    """
    #page = request.args.get('page', 1, type=int)
    posts = post_rep.find_posts()
    following_users = []
    if current_user.is_authenticated:
        following_users = user_rep.get_following_as_list_of_users(current_user)

    return render_template("home.html", title="Home", posts=posts, following_users=following_users)


@main.route("/about")
def about():
    """
    Route handler for the about page.

    Returns:
        str: Rendered template for the about page.
    """
    return render_template("about.html", title="About")


@main.route("/search", methods=['GET', 'POST'])
def search():
    """
    Route handler for the search page.

    Returns:
        str: Rendered template for the search page.
    """
    if request.method == 'POST':
        query = request.form.get('search_input')
    else:
        query = request.args.get('query')

    posts = post_rep.search_posts(query)
    users = user_rep.search_users(query)
    return render_template("search_results.html", title="Search", posts=posts, users=users, query=query)
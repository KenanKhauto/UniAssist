

from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app
from application.custom import user_rep, post_rep

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
    for post in posts:
        post.author = user_rep.find_user_by_id(post.author)
    
    

    return render_template("home.html", title="Home", posts=posts)


@main.route("/about")
def about():
    """
    Route handler for the about page.

    Returns:
        str: Rendered template for the about page.
    """
    return render_template("about.html", title="About")

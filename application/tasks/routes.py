

from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app
from application.custom import user_rep, post_rep

tasks = Blueprint('tasks', __name__)


@tasks.route("/my_tasks")
def my_tasks():
    """
    Route handler for the tasks page.

    Returns:
        str: Rendered template for the tasks page.
    """
    #page = request.args.get('page', 1, type=int)
    #tasks = task_rep.find_tasks()

    return render_template("my_tasks.html", title="Tasks")
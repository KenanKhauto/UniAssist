

from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app, jsonify
from application.custom import user_rep, post_rep
from flask_login import login_required, current_user

tasks = Blueprint('tasks', __name__)


@tasks.route("/my_tasks")
@login_required
def my_tasks():
    """
    Route handler for the tasks page.

    Returns:
        str: Rendered template for the tasks page.
    """

    tasks = user_rep.find_tasks_by_user_id(current_user)

    return render_template("my_tasks.html", title="Tasks", tasks=tasks)


@tasks.route("/add_task", methods=['POST'])
@login_required
def add_task():
    """
    Route handler for the tasks page.

    Returns:
        str: Rendered template for the tasks page.
    """
    data  = request.get_json()
    user_rep.add_task_by_user_id(current_user, data['description'])
    result = {"success": True, "response": "Done"}
    return jsonify(result)


@tasks.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            user_rep.update_task_status(task_id ,current_user, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            user_rep.update_task_description(task_id, current_user, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@tasks.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry updates """
    try:
        user_rep.delete_task_from_user_by_id(current_user, task_id)
        result = {'success': True, 'response': 'Task Deleted'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

from flask import Blueprint

from flask import render_template, request, redirect, Blueprint, flash, url_for, jsonify
from application import bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from application.custom import user_rep, post_rep
from flask_login import login_user, current_user, logout_user, login_required
from .utils import save_picture
from .models import User

users = Blueprint('users', __name__)



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


@users.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
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
    if form.validate_on_submit():
        user = user_rep.find_user_by_email(email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", category="success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check email and password", category="danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            user_rep.update_user_image(current_user)

        current_user.email = form.email.data
        current_user.username = form.username.data

        user_rep.update_user_username(current_user)
        user_rep.update_user_email(current_user)

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    posts = post_rep.find_posts_by_author(current_user.id)
    return render_template('account.html', title='Account',
                           image_file=image_file, 
                           form=form, 
                           posts=posts)


@users.route("/user/<int:user_id>")
def user_profile(user_id):
    try:
        if current_user.id == user_id:
            return redirect(url_for('users.account'))
    except:
        print("something went wrong")
    
    posts = post_rep.find_posts_by_author(user_id)
    user = user_rep.find_user_by_id(user_id)
    username = user.username
    email = user.email
    image_file = user.image_file

    is_following = current_user.id in user.followers

    return render_template('user_profile.html', title='Account',
                            image_file=image_file, 
                            posts=posts,
                            username=username,
                            email=email,
                            user_id=user_id,
                            is_following=is_following)


@users.route("/follow/<int:user_id>", methods=["POST", "GET"])
@login_required
def follow(user_id):
    target = user_rep.find_user_by_id(user_id)
    if not target:
        return jsonify({'error': 'User not found'}), 404
    #target_user = User(target)
    current_user.follow(target)
    return jsonify({'message': f'You are now following {target.username}'}), 200

@users.route('/unfollow/<int:user_id>', methods=['POST', "GET"])
@login_required
def unfollow(user_id):
    target = user_rep.find_user_by_id(user_id)
    if not target:
        return jsonify({'error': 'User not found'}), 404
    #target_user = User(target)
    current_user.unfollow(target)
    return jsonify({'message': f'You have unfollowed {target.username}'}), 200
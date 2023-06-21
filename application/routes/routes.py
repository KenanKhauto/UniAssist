import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app
from application import login_manager, bcrypt
from application.routes.forms import RegistrationForm, LoginForm, UpdateAccountForm,AddBookForm
from application.custom import user_rep, book_rep
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

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


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print(current_user.username)
    print(image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)




@main.route("/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    books_user = book_rep.find_books_per_user(current_user.id)
    print(books_user)
    if form.validate_on_submit():
        pdf_file = form.book_file.data
        file_name = secure_filename(form.book_file.data.filename)
        pdf_path = os.path.join(current_app.root_path, 'static/books', file_name)
        pdf_file.save(pdf_path)
        book_dic = {"book_name":form.book_name.data, "book_file":file_name, "user_id":current_user.id}
        request_bool = book_rep.save_book_in_DB(book_dic)
        if request_bool:
            flash("Your book has been added successfuly!", category="success")
            return redirect(url_for("main.add_book"))
        else:
            flash("You already have this book!", category='info')
            return redirect(url_for("main.add_book"))
   
    return render_template("add_book.html", titel="Add a book", form=form, books_user=books_user)


@main.route("/view_book", methods=['GET', 'POST'])
@login_required
def view_book():
    return render_template('bookview.html')
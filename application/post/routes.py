from flask import Blueprint, flash, redirect, url_for, render_template, request, abort
from .forms import PostForm
from application.custom import post_rep
from flask_login import current_user, login_required
from datetime import datetime
from application.database.models import Post

post = Blueprint('post', __name__)


@post.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    post = Post(id=1, title=form.title.data, content=form.content.data, author=current_user, date_posted=datetime.utcnow())
    print(current_user.username)
    if form.validate_on_submit():
        post_rep.insert_post(title=form.title.data, content=form.content.data, author=current_user, date_posted=datetime.utcnow())
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('new_post.html', title='New Post', form=form, legend='New Post', post=post)

'''
@post.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@post.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@post.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@post.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
'''
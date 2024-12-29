"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    """Homepage redirects to 5 most recent posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts_homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# //////////////////////////////////////////////////
# USERS SECTION

@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user_list.html", users=users)

@app.route('/users/new', methods = ["GET"])
def add_user_form():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} added")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect('/users')

# //////////////////////////////////////////////////////////////////
# POSTS SECTION
@app.route('/users/int:user_id>/posts/new')
def new_post_form(user_id):

    user  = User.query.get_or_404(user_id)
    return render_template('new_posts.html', user=user)

@app.route('/users/int:user_id>/posts/new', methods = ['POST'])
def new_posts(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content = content, user_id=user.id)
    
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")
    

@app.route('/posts/<int:post_id>')
def posts_detail(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('edit_posts.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a specific post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')
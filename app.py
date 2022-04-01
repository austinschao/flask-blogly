"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, DEFAULT_IMG_URL
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret-pw'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def display_user_listing():
    """ Display User Listing Page """

    return redirect('/users')

@app.get('/users')
def display_all_users():
    """ Display each user, convert their names to links to the view their page
        and have a link to add-user """

    # display all users
    users = User.query.all()

    return render_template('user_listing.html', users=users)

@app.get('/users/new')
def display_add_form():
    """ Display a form to create a new user """

    return render_template('new_user_form.html')

@app.post('/users/new')
def create_new_user():
    """ Retrieve data from form and sends user info to database """

    response = request.form
    image_url = response['image_url'] or None

    new_user = User(first_name = response['first_name'], last_name = response['last_name'],
        image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def display_user_page(user_id):
    """ Display a given user's page """

    curr_user = User.query.get_or_404(user_id)
    posts = curr_user.posts



    return render_template('user_detail_page.html', curr_user = curr_user, posts = posts)

@app.post('/users/<int:user_id>/delete/')
def delete_user(user_id):
    """Deletes the user's page"""
    user = User.query.get_or_404(user_id)
    Post.query.filter(Post.user_id == user_id).delete()

    User.query.filter_by(id = user_id).delete()
    db.session.commit()

    flash(f'User "{user.first_name} {user.last_name}" was successfully deleted.')
    return redirect('/users')

@app.get('/users/<int:user_id>/edit')
def display_edit_page(user_id):
    """ Display edit page """

    curr_user = User.query.get_or_404(user_id)
    return render_template('user_edit_page.html', curr_user = curr_user)

@app.post('/users/<int:user_id>/edit')
def update_user_profile(user_id):
    """Updates user profile with new information"""

    response = request.form

    curr_user = User.query.get_or_404(user_id)
    image_url = response['image_url'] or DEFAULT_IMG_URL
    if response['first_name']:
        curr_user.first_name = response['first_name']
    if response['last_name']:
        curr_user.last_name = response['last_name']
    if response['image_url'] or DEFAULT_IMG_URL:
        curr_user.image_url = image_url

    db.session.commit()
    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def display_post_form(user_id):
    """ Display post form """

    curr_user = User.query.get_or_404(user_id)

    return render_template('add_post.html', curr_user=curr_user)


@app.post('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """ Add new post """

    response = request.form
    title = response['title']
    content = response['content']
    curr_user = User.query.get_or_404(user_id)

    new_post = Post(title = title, content = content, user_id = curr_user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{curr_user.id}")


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Displays the user post that was clicked on"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_detail_page.html', post=post, curr_user=post.user)


@app.get('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Displays form to edit a selected post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_edit_page.html', post = post)


@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """"Handle post edit"""

    response = request.form
    title = response["title"]
    content = response["content"]

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the selected post"""

    post = Post.query.get_or_404(post_id)
    user = User.query.filter(User.id == post.user_id).first()

    Post.query.filter_by(id = post_id).delete()

    db.session.commit()

    flash("Message successfully deleted!")
    return redirect(f'/users/{user.id}')


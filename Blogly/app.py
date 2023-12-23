"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, default_image_url, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bloggytime3983241__'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_ECHO'] = True


# app.config['DEBUG_TB_ENABLED'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home_page():
  """Displays lists of posts sorted by: latest-oldest """
  posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
  return render_template('posts_list.html', posts=posts)


###### USER ##########


@app.route('/users')
def users_list():
  """List all Users"""
  users = User.query.all()
  # deleted_user_id = session.get('deleted_user_id')

  # if deleted_user_id:
  #   session.pop('deleted_user_id', None)
  return render_template('users_list.html', users=users)


@app.route('/users/form', methods=["GET"])
def add_user():
  """Display form to add/ create new User"""
  flash("Complete to create a new User", category="general")
  return render_template('new_user_form.html')


@app.route('/users/form', methods=["POST"])
def get_form_data():
  """Handle form submission"""
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url'] or None

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()

  flash(f'User: {new_user.full_name()} created', "success")
  # return redirect (f"/users/{new_user.id}")
  return redirect ('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
  """Display details about a single user."""
  user = User.query.get_or_404(user_id)
  # post = Post.query.get_or_404(user_id)

  flash("""**Note:\nDeleting a user is irreversible.\n
  Please proceed with caution.""", category="warning")
  return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user_info(user_id):
  """Edit existing User"""
  user = User.query.get_or_404(user_id)
  
  flash (f"Edit {user.full_name()}'s Profile", category='general')
  return render_template('edit_user_info.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_info(user_id):
  """updates edited user info / handle form submission"""
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url'] if request.form['image_url'] else default_image_url

  db.session.add(user)
  db.session.commit()

  flash(f"User: {user.full_name()} info has been edited",category="success")
  return redirect(f"/users/{user.id}")
  # return redirect ('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  """delete user info"""
  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  flash(f"User: {user.full_name()}'s profile has been deleted ", category="success")
  return redirect('/users')
  

###### POST ##########

@app.route('/users/<int:user_id>/posts/form', methods=['GET'])
def create_post(user_id):
  """Display form to add a post for specfic user. """
  user = User.query.get_or_404(user_id)
  return render_template('post_form.html', user=user)



# user form data is retrieved , user redirected to USER DETAILS page
@app.route('/users/<int:user_id>/posts/form', methods=['POST'])
def add_post (user_id):
  """Handle form submission, add post, redirect to user page """
  user= User.query.get_or_404(user_id)
  new_post = Post(title=request.form['title'],
                               content=request.form['content'], 
                               user=user)
  db.session.add(new_post)
  db.session.commit()

  flash(f'Post successfully posted', "success")

  return redirect (f"/users/{user_id}")



# from user details page, user clicks TITLE OF POST
# redirect user to POST DETAILS page (post_id)
@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
  """Displays a post with buttons to edit and delete the post"""
  post = Post.query.get_or_404(post_id)
  return render_template('post_detail.html', post=post)


# option to edit post (redirect to edit post page)
# delete(return redirect (f"/users/{user_id}"))
# cancel (return redirect (f"/users/{user_id}"))
@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def get_post_edit(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post_edit.html', post=post)

#post request after editing post
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  db.session.add(post)
  db.session.commit()

  return redirect(f"/users/{post.user_id}")



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
  """Delete post"""
  post = Post.query.get_or_404(post_id)

  db.session.delete(post)
  db.session.commit()

  flash(f'{post.title} deleted', category='success')
  return redirect(f"/users/{post.user_id}")

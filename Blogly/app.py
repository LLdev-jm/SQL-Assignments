"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, default_image_url

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bloggytime3983241__'
# app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'bloggytime3983241__'
# app.config['DEBUG_TB_ENABLED'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home_page():
  return redirect('/users')


@app.route('/users')
def users_list():
  """List all Users"""
  users = User.query.all()
  deleted_user_id = session.get('deleted_user_id')

  if deleted_user_id:
    session.pop('deleted_user_id', None)
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
  


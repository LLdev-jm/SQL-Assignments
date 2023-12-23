from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db_blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

default_image_url = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"

class UserViewsTestCase(TestCase):
  """Tests for view functions for Users"""

  def setUp(self):
    """Adding sample user"""
    self.app = app.test_client()
    User.query.delete()

    # users = User.query.all()
    user1 = User(first_name='Jane', last_name='Doe', image_url=default_image_url)
    user2 = User(first_name='John', last_name='Doe', image_url=default_image_url)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # self.user_id = user1.id
    self.user_id = user2.id

  def tearDown(self):
      """Clean up any fouled transaction"""

      # User.query.delete()
      db.session.rollback()

  def test_users_list(self):
     with app.test_client() as client:
        response = client.get('/users')
        html= response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        # self.assertIn('Jane Doe', html)
        self.assertIn('John Doe', html)

  def test_user_details(self):
     with app.test_client() as client:
        response = client.get(f'/users/{self.user_id}')
        html = response.get_data(as_text=True)
        
        print("User ID:", self.user_id)
        print(" HTML:", html)

        self.assertEqual(response.status_code,200)
        # self.assertIn('<h1>ABOUT Jane Doe</h1>', html)
        self.assertIn('<h1>ABOUT John Doe</h1>', html)
        print(" HTML:", html)

  def test_update_info(self):
     user_id = self.user_id

     form_data = {
        'first_name': 'Choco',
        'last_name': 'Yum',
        'image_url': default_image_url
     }

     response = self.app.post(f'/users/{user_id}/edit', data=form_data)
     print(f"test_update_info:",response.status_code)

     self.assertEqual(response.status_code, 302)

    #  redirected_response = self.app.get(response.location)
    #  self.assertIn('Choco Yum', redirected_response.get_data(as_text=True))
  
    #  updated_user = User.query.get(user_id)
    #  self.assertIsNotNone(updated_user)
    #  self.assertEqual(updated_user.first_name, 'Choco')
    #  self.assertEqual(updated_user.last_name, 'Yum')
    #  self.assertEqual(updated_user.image_url, default_image_url)



  def test_delete_user(self):
    """delete user completely"""

    user_id = self.user_id
    response = self.app.post(f'/users/{user_id}/delete')

    print(f"test delete user:",response.status_code)
    self.assertEqual(response.status_code, 302)

    deleted_user = User.query.get(user_id)
    self.assertIsNone(deleted_user)
    response=self.app.get('/users')
    html = response.get_data(as_text=True)

    # self.assertIn('<a href="/users">/users</a>', html)

    
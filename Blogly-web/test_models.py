from unittest import TestCase

from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

default_image_url = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"

class ClassModelTestCase(TestCase):
  """Tests for model for Users Class"""
  def setUp(self):
    """Clean up any existing pets"""

    User.query.delete()

  def tearDown(self):
    """Clean up any fouled transaction"""

    db.session.rollback()


  def test_full_name(self):
    users = User.query.all()
    user1 = User(first_name='Jane', last_name='Doe', image_url=default_image_url)
    user2 = User(first_name='John', last_name='Doe', image_url=default_image_url)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    self.assertEqual(user1.full_name(), "Jane Doe")
    self.assertEqual(user2.full_name(), "John Doe")
  

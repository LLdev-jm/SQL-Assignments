"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image_url = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_image_url)
    
    def __repr__ (self):
        u = self
        return f"<User id = {u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    
    def full_name (self):
        return f"{self.first_name} {self.last_name}"
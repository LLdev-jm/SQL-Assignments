"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


default_image_url = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_image_url)
    posts = db.relationship('Post', backref='user', cascade='all,delete-orphan')
    
    def __repr__ (self):
        u = self
        return f"<User id = {u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    
    def full_name (self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
                                                                                                #datetime module datetime class now attribute
    

    @property
    def dt_formatting(self):
        """Return formatted date and time for each post."""

        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')
    
def connect_db(app):
    db.app = app
    db.init_app(app)


class PostTag(db.Model):
    __tablename__='posts_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_tags", backref="tags")

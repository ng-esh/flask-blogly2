"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
default_img_url = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """site user"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30), 
                           nullable = False)
    
    last_name = db.Column(db.String(30), 
                          nullable = False)
    
    image_url = db.Column (db.String, nullable = True, 
                           default = default_img_url)
    posts = db.relationship('Post', backref = 'user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"
    
    # def __repr__(self):
    #     return f"<User {self.full_name} {self.image_url}>"

class Post(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable = False)
    
    content = db.Column(db.Text, 
                        nullable = False)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.id"), nullable = False)
   
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.now)
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.user_id}>"
    
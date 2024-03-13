from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from sqlalchemy.orm import relationship

## Modelos ##
db = SQLAlchemy()


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_img = db.Column(db.String(100), nullable=True, default='default.jpg')

    posts = db.relationship('Posts', back_populates='user')
    comments = relationship("Comments", backref="Author")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="posts")



class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user = relationship("Users", back_populates="comments")

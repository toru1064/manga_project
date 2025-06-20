from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='books')
    likes = db.relationship('Like', backref='book', cascade="all, delete", lazy='dynamic')
    comments = db.relationship('Comment', backref='book', cascade='all, delete', lazy='dynamic')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    likes = db.relationship('Like', backref='user', cascade="all, delete", lazy='dynamic')

    # プロフィール情報
    profile_image = db.Column(db.String(256), nullable=True)
    display_name = db.Column(db.String(64), nullable=True)
    bio = db.Column(db.Text)

    # パスワード設定用メソッド
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # パスワード確認用メソッド
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    user = db.relationship('User', backref='Book_comments')
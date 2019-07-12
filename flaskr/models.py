from datetime import datetime
from flaskr.db import db 



class User(db.Model):
    # CREATE TABLE user (
    #   id INTEGER PRIMARY KEY AUTOINCREMENT,
    #   username TEXT UNIQUE NOT NULL,
    #   password TEXT NOT NULL
    # );
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)


class Post(db.Model):
    # CREATE TABLE post (
    #   id INTEGER PRIMARY KEY AUTOINCREMENT,
    #   author_id INTEGER NOT NULL,
    #   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #   title TEXT NOT NULL,
    #   body TEXT NOT NULL,
    #   FOREIGN KEY (author_id) REFERENCES user (id)
    # );
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(256), nullable=False)

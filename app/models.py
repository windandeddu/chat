from app import app
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_id1 = db.relationship('Conversation_users', lazy='dynamic')
    user_id2 = db.relationship('Messages', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format((self.username))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.String())
    last_message_datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    conversation_id1 = db.relationship('Conversation_users', backref='user', lazy='dynamic')
    conversation_id2 = db.relationship('Messages', backref='user', lazy='dynamic')


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.ForeignKey('conversation.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    text = db.Column(db.Text())
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Conversation_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    conversation_id = db.Column(db.ForeignKey('conversation.id'))
    read = db.Column(db.Boolean, default=False)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
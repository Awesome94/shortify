from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import datetime

from app import app
from flask_login import LoginManager, UserMixin

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(90))
    url = db.relationship('UrlSchema', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.password = password

    def is_authenticated(self):
        '''return true if the user is authenticated'''
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        '''since anonymous users are not supported, it will return false for anonymous users'''
        return False
        
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UrlSchema(db.Model):
    __tablename__ = "urlsSchema"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    long_url = db.Column(db.String(255))
    short_url = db.Column(db.String(100), unique=True)
    clicks = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

   
    def __init__(self, long_url):
        self.long_url = long_url

    def __repr__(self):
        return '<url {}>'.format(self.short_url)


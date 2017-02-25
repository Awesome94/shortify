from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import datetime

from app import app
from flask_login import LoginManager, UserMixin

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="pg_db_username", DB_PASS="pg_db_password", DB_ADDR="pg_db_hostname", DB_NAME="pg_db_name")
db = SQLAlchemy(app)

class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()
    
    def update(self):
        return db.session.commit()
    
    def delete(self):
        db.session.delete(resource)
        return db.session.commit()

class User(UserMixin, db.Model, CRUD):
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

class UsersSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    email = fields.Email(validate=not_blank)
    username = fields.String(validate=not_blank)
    password = fields.String(validate=not_blank)
     
     
     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}
 
    class Meta:
        type_ = 'users'

  
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
        # self.short_url = short_url

    def __repr__(self):
        return '<url {}>'.format(self.short_url)


class LinkSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    title = fields.String()
    long_url = fields.String(validate=not_blank)
    short_url = fields.String(validate=not_blank)
    active = fields.Boolean()
    clicks = fields.Integer()
    aurthor_id = fields.Integer()
    timestamp = fields.DateTime()
     
    #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/links/"
        else:
            self_link = "/links/{}".format(data['id'])
        return {'self': self_link}
 
    class Meta:
        type_ = 'links'


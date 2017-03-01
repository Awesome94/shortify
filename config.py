# pagination
POSTS_PER_PAGE = 5

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = os.environ.get('DEBUG', False)
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'some secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # HASH_ROUNDS = 100000 for password hashing


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    
    # HASH_ROUNDS = 1 will be applied incase password hashing is implemented
from flask_testing import TestCase
from app import app
from config import TestingConfig
from models.models import User, db

class BaseTestConfig(TestCase):
    
    def create_app(self):
        app.config.from_object(TestingConfig)
        return app
    
    def setUp(self):
        db.create_all()
        user = User(
            username="user1",
            email="test1@user.com",
            password="just_a_test_user",
        )
        db.session.add(user)
        db.session.commit()
    
    def teardown(self):
        db.session.remove()
        db.drop_all()


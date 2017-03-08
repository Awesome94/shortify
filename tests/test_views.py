from .test_base import BaseTestConfig
from flask_login import current_user
from models.models import User, db
from flask import url_for
import unittest

class TestUserViews(BaseTestConfig):
    
    def test_index_page_loads(self):
        response = self.client.get('/index')
        self.assertIn(b'Shortify', response.data)

    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="sample@example.com", password="just_test_user"),
            )
            self.assert_redirects(response, url_for('create_short'))
        
    def test_user_registration(self):
        users = User.query.all()
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username="awesome", email="awesome@test.com", password="password",
                password2="password"),
                follow_redirects=True
            )
            new_count_users = User.query.all()
            self.assertEqual(len(new_count_users), len(users)+1)
    
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertTrue(current_user.is_anonymous)

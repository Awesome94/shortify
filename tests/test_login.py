from .test_base import BaseTestConfig
from flask import url_for

from models.models import User 

class UserViewTests(BaseTestConfig):
    
    def test_users_can_login(self):
        response = self.client.post(url_for('login'),
                                    data={'email': User.email, 'password': User.password})
        self.assertEqual(response.status_code, 302)
        self.assert_redirects(response, url_for('create_short'))
        db.session.remove()
        db.drop_all()

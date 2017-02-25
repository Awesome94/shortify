from .test_base import BaseTestConfig
# from shortify.models import db
# from config import basedir
from flask import url_for

from models.models import User 

class UserViewTests(BaseTestConfig):
    
    def test_users_can_login(self):
        # user = User('Josse34', 'joe@joes.com', '12345')
        # db.session.add(user)
        # db.session.commit()
        # import ipdb; ipdb.set_trace()
        response = self.client.post(url_for('login'),
                                    data={'email': User.email, 'password': User.password})
        # self.assert_redirects(response, url_for('login'))
        self.assertEqual(response.status_code, 302)
        self.assert_redirects(response, url_for('create_short'))
        db.session.remove()
        db.drop_all()
    

    # def test_register_user(self):
    #     pass
        
    
    # def test_invalid_password(self):
    #     pass

    # def test_url_shorten_when_user_logged_in(self):
    #     pass
    
    # def test_most_influential_users(self):
    #     pass

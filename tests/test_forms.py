from .test_base import BaseTestConfig
from forms.forms import UrlForm, LoginForm, UpdateUrlForm, RegisterForm

class TestUserForms(BaseTestConfig):
    ''' 
    This class will inherit properties from the BaseTestConfig class 
    to test whether the form passes or fails validation 
    based on the data entered.
    
    '''

    def test_validate_success_register_form(self):
        form = RegisterForm(username='awesome', 
                            email='allan@gmail.com', password='password', password2='password')
        self.assertTrue(form.validate())
    
    def test_invalid_password_format(self):
         form = RegisterForm(username='awesome', 
                            email='allan@gmail.com', password='password', password2='different')
         self.assertFalse(form.validate())
        
    def test_email_already_registered(self):
         form = RegisterForm(email='allan@gmail.com', password='password', password2='password')
         self.assertFalse(form.validate())
    
    def test_validate_on_login(self):
        form = LoginForm(email='test@example.com',password = 'password')
        self.assertTrue(form.validate())
    
    def test_login_without_password(self):
        form=LoginForm(email='test@example.com', password='')
        self.assertFalse(form.validate())
    
    def test_login_without_email(self):
        form=LoginForm(email='', password='password')
        self.assertFalse(form.validate())
    
    def test_no_email_no_password(self):
        form = LoginForm(email='', password='')
        self.assertFalse(form.validate())
    
    def test_url_field_blank(self):
        form=UrlForm(url='')
        self.assertFalse(form.validate())
   

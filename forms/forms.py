from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, url,
                                length, EqualTo)
from wtforms.fields.html5 import URLField

class RegisterForm(FlaskForm):
    # creating a registration form with the relevant fields required to register a user
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                message=("username should be one word, letters, numbers, and underscores only,")
                )])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=2),
            EqualTo('password2', message='passwords must match')])

    password2 = PasswordField(
        'confirm Password',
        validators=[DataRequired()])
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email =  StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    submit = SubmitField('Login')
                

class UrlForm(FlaskForm):
    url = URLField('Url', validators=[DataRequired(), url()])
    shorturl = StringField('Short Url')
    vanity_string = StringField('vanity string')
    submit = SubmitField('Shorten')
    status = BooleanField()

class UpdateUrlForm(FlaskForm):
    long_url = URLField('Url',validators=[DataRequired(), url()])
    submit = SubmitField('Update')

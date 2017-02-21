from flask import Flask, render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app
from forms import forms
from models import User, UrlSchema, db
import short_url as sh_url
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.sql import func, desc
import timeago, datetime
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import lxml.html
# from app import SITE_URL
from config import POSTS_PER_PAGE


 
db.create_all()
db.session.commit()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    #loads the user when needed for login.
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def create_short(page=1):
    '''creating a short url from a given long url'''
    login_form = forms.LoginForm()
    update_form = forms.UpdateUrlForm()
    register_form = forms.RegisterForm()
    form = forms.UrlForm()
    url = form.url.data 
    # print (url)
    custom_url = form.vanity_string.data
    current_id = current_user.get_id()
    
    #The Url variable holds the original url data which is passed to generate a short Url
    data = UrlSchema.query.filter_by(author_id=current_id).paginate(page, POSTS_PER_PAGE, False)

    # get frequent users
    frequent_users = get_frequent_users()
    
    #popular links i.e links with most clicks (above and equal to 3)
    pop_link = get_popular_links()
   
    #latest links added 
    recent_links = get_recent_links()

    if request.method=='POST'and form.validate_on_submit():
        new_long_url=UrlSchema(url) 
        # t = lxml.html.parse(urlopen(url))
        new_long_url.author_id = current_id
        new_long_url.timestamp = datetime.datetime.utcnow()
        #adding url title
        # url_title =  (t.find(".//title").text)
        # new_long_url.title = url_title
        db.session.add(new_long_url)
        db.session.commit()
        if custom_url:
            url_short = custom_url
            new_long_url.short_url=url_short
            db.session.commit()
        else:
            url_short = sh_url.encode_url(new_long_url.id)
            new_long_url.short_url=url_short
            db.session.commit()
        return render_template('index.html', form=form, update_form=update_form, login_form=login_form, url_short=url_short, data=data, pop_link=pop_link, recent_links=recent_links, register_form=register_form)    
    return render_template('index.html', form=form, update_form=update_form, data=data, frequent_users=frequent_users, pop_link=pop_link, recent_links=recent_links, login_form=login_form, register_form=register_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''This functionallows users to register. Heence will add users to the system.'''
    register_form = forms.RegisterForm()
    username = register_form.username.data
    email = register_form.email.data
    password = register_form.password.data
    if request.method == 'POST' and form.validate_on_submit():
        new_user=User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for('create_short'))
    return render_template('register.html', register_form=register_form)


@app.route('/login', methods=['POST','GET'])
def login():
    login_form = forms.LoginForm()
    if request.method =='POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        print('steve')
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            login_user(user)
            g.user = user
           
            return redirect (url_for('create_short'))
             #upon login, users will be directed to the url for 'create_short'
    return render_template('login.html', login_form=login_form)

# @app.route('logged_in', methods=['GET','POST'])
# def home():
#     return render_template('home.html', form=form)

@app.route('/<url_short>')
def display(url_short):
    original_url = UrlSchema.query.filter_by(short_url=url_short).first()
    print(original_url)
    original_url.clicks = original_url.clicks+1
    db.session.add(original_url)
    db.session.commit()
    if original_url.active:
        return redirect(original_url.long_url)
    else:
        return render_template('error-Inactive.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged Out Successfully.")
    return redirect (url_for('login'))

def get_frequent_users():
    results = db.session.query(UrlSchema.author_id, 
        db.func.count(UrlSchema.author_id).label('count')).filter(UrlSchema.author_id.isnot(None)).group_by(UrlSchema.author_id).all()
    data = []
    for result in results:
        user = User.query.filter_by(id=result.author_id).first()
        data.append({'name': user.username, 'count': result.count})
    return data

def get_popular_links():
     pop_link  = db.session.query(UrlSchema).filter(UrlSchema.clicks>=2).all()
     data = []
     for link in pop_link:
         data.append({'url': link.short_url, 'clicks': link.clicks, 'url_title':link.title})
     return data

@app.route('/rec', methods = ['GET', 'POST'])
def get_recent_links():
    now = datetime.datetime.now()
    recent_link = db.session.query(UrlSchema).order_by(desc(UrlSchema.id)).limit(5)
    data = []
    for link in recent_link:
        data.append({'rec_link': link.short_url, 'url_title': link.title, 'date_added': (timeago.format(link.timestamp, datetime.datetime.now())) })
    return data

@app.route('/delete/', methods=['GET','POST'])
def delete_link():
    id = request.form.get('link-id')
    url = UrlSchema.query.filter_by(id=id).first()
    db.session.delete(url)
    db.session.commit()
    return redirect(url_for('create_short'))

@app.route('/change-status/<url_id>')
def change_status(url_id):
    url = UrlSchema.query.filter_by(id=url_id).first()
    url.active = not url.active
    db.session.commit()
    return redirect(url_for('create_short'))

@app.route('/edit/', methods=['GET','POST'])
@login_required
def update():
    id = request.form.get('url-id')
    update_form = forms.UpdateUrlForm()
    if request.method=='POST'and update_form.validate_on_submit():
        url = UrlSchema.query.filter_by(id=id).first()
        url.long_url = update_form.long_url.data
        db.session.commit()
        flash('Your changes have been saved.')
    return redirect (url_for('create_short'))





            
        
    
    
# @app.route('/tyto', methods=['GET','POST'])
# def urltitle():
#     title = db.session.query(UrlSchema).all()    
#     #fetch html
#     data = []
#     for titles in title:
#         source = urllib.request.urlopen(titles.long_url)
#         BS = BeautifulSoup(source)
#         Heading = (BS.find('title').text)
#         data.append({'title': Heading})
#     print (data)
#     return "yos"
    # #parse with BeautifulSoup
    
    # #create a variable  for the title in the URL
   
    # print (Heading)
    # return "Heading"


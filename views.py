from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, Markup
import short_url as sh_url
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.sql import func, desc
import timeago, datetime
from config import POSTS_PER_PAGE
from app import app
from forms.forms import UrlForm, LoginForm, UpdateUrlForm, RegisterForm
from models.models import User, UrlSchema, db, LinkSchema, UsersSchema
from functools import wraps


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    #loads the user when needed for login.
    return User.query.get(int(user_id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('create_short', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def create_short(page=1):
    '''creating a short url from a given long url'''
    login_form = LoginForm()
    update_form = UpdateUrlForm()
    register_form = RegisterForm()
    form = UrlForm()
    url = form.url.data 
    # print (url)
    custom_url = form.vanity_string.data
    current_id = current_user.get_id()
    
    #The Url variable holds the original url data which is passed to generate a short Url
    data = UrlSchema.query.filter_by(author_id=current_id).order_by(desc(UrlSchema.id)).paginate(page, POSTS_PER_PAGE, False)
    url_short = None

    if request.method=='POST' and form.validate_on_submit():
        if len(url)>100:
            flash("Invalid entry Url too long!!!.", 'error')
        else:                                
            new_long_url=UrlSchema(url) 
            db.session.add(new_long_url)
            db.session.commit()
            new_long_url.author_id = current_id
            #adding url title by spliting the original long url
            url_title = url.split("/")[2:3]
            """removing curly brackets from the url title """
            new_long_url.title = (', '.join(url_title))
            # if there is no custom url the short url will be genrated randomly
            new_long_url.short_url = custom_url if custom_url else sh_url.encode_url(new_long_url.id)
            url_short = new_long_url.short_url
            db.session.commit()
            form = UrlForm(formdata=None)

    # get frequent users
    frequent_users = get_frequent_users()
    #popular links i.e links with most clicks (above and equal to 3)
    pop_link = get_popular_links()
    #latest links added 
    recent_links = get_recent_links()
    return render_template('index.html', form=form, update_form=update_form, data=data, frequent_users=frequent_users, pop_link=pop_link, url_short=url_short, recent_links=recent_links, login_form=login_form, register_form=register_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''This functionallows users to register. Heence will add users to the system.'''
    register_form = RegisterForm()
    username = register_form.username.data
    email = register_form.email.data
    password = register_form.password.data
    if request.method == 'POST' and register_form.validate_on_submit():
        new_user=User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful')
        return redirect (url_for('create_short'))
    else:
        flash("Make sure all fields are filled with valid data")    
    return render_template('register.html', register_form=register_form)


@app.route('/login', methods=['POST','GET'])
def login():
    login_form = LoginForm()
    if request.method =='POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            login_user(user)
            g.user = user
            message = Markup("<h5>logged in successfully</h5>")
            flash(message)
            return redirect (url_for('create_short'))
        else:
            flash('Invalid credentials Try again','error')
    return redirect (url_for('create_short'))


@app.route('/<url_short>')
def display(url_short):
    # Redirects the short Url to the original URL
    original_url = UrlSchema.query.filter_by(short_url=url_short).first()
    # db.session.query(UrlSchema).filter_by(short_url=url_short).first()
    print(original_url)
    original_url.clicks = original_url.clicks+1
    db.session.add(original_url)
    db.session.commit()
    if original_url.active:
        return redirect(original_url.long_url)
    else:
        return render_template('error-Inactive.html')

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    message = Markup("<h5>Logged Out Successfully.</h5>")
    flash (message)
    return redirect (url_for('create_short'))

def get_frequent_users():
    # Returns most frequent or influential users depending on the number of urls they have shortened.
    results = db.session.query(UrlSchema.author_id, 
        db.func.count(UrlSchema.author_id).label('count')).filter(UrlSchema.author_id.isnot(None)).group_by(UrlSchema.author_id).all()
    data = []
    for result in results:
        user = User.query.filter_by(id=result.author_id).first()
        data.append({'name': user.username, 'count': result.count})
    return data

def get_popular_links():
    # Returns most popular links depending on the number of clicks 
     pop_link  = db.session.query(UrlSchema).filter(UrlSchema.clicks>=5).all()
     data = []
     for link in pop_link:
         data.append({'url': link.short_url, 'clicks': link.clicks, 'url_title':link.title})
     return data

def get_recent_links():
    # function will return the most recent links according to the date they where added
    now = datetime.datetime.now()
    recent_link = db.session.query(UrlSchema).order_by(desc(UrlSchema.id)).limit(5)
    data = []
    for link in recent_link:
        data.append({'rec_link': link.short_url, 'url_title': link.title, 'date_added': (timeago.format(link.timestamp)) })
    return data

@app.route('/delete', methods=['GET','POST'])
def delete_link():
    # function will enable a Logged in User to delete any url of there choice from the table
    id = request.form.get('link-id')
    url = UrlSchema.query.filter_by(id=id).first()
    db.session.delete(url)
    db.session.commit()
    return redirect(url_for('create_short'))

@app.route('/change-status/<url_id>')
def change_status(url_id):
    # Allows activating a deactivating a link to logged in Users
    url = UrlSchema.query.filter_by(id=url_id).first()
    url.active = not url.active
    db.session.commit()
    return redirect(url_for('create_short'))

@app.route('/edit/', methods=['GET','POST'])
def update():
    # Enables user to change target Url but maintain the short Url
    id = request.form.get('url-id')
    update_form = UpdateUrlForm()
    if request.method=='POST'and update_form.validate_on_submit():
        url = UrlSchema.query.filter_by(id=id).first()
        url.long_url = update_form.long_url.data
        db.session.commit()
        flash('Your changes have been saved.')
    return redirect (url_for('create_short'))


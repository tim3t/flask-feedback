from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "f33db@ck"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

# ~~~~~~  ROUTES  ~~~~~~ #

@app.route('/')
def redirect_home():
    """If user visits / root route, redirect to /register"""
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    """Display a form that when submitted creates a user"""
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.register(username, password, first_name, last_name, email)
        db.session.commit()
        session['username'] = user.username
        flash('Successfully created your account!')
        return redirect('/secret')

    else:
        return render_template('register.html', form=form)

@app.route('/secret')
def show_secret_page():
    """After register or validation, show secret page"""
    if 'username' not in session:
        flash('Please login first!')
        return redirect('/login')
    if 'username' in session:

        return render_template('secret.html')

@app.route('/login', methods = ['GET', 'POST'])
def handle_login_form():
    """Show and handle log-in form submissions"""
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            flash(f"Welcome back, {user.username}!")
            session['username'] = user.username
            return redirect ('/secret')
        else:
            form.username.errors = ['Invalid username or password.']
    
    return render_template('login.html', form=form)
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

@app.route('/register')
def register_user():
    """Display a form that when submitted creates a user"""
    return render_template('register.html')


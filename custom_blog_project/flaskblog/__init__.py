from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY']='515ca6823d291bbb1108a59da2e7a3e2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)   #configr our flask app to work with flask_login
login_manager.login_view='login' #'login' is function name of route  #dint understand
login_manager.login_message_category='info' #info is a bootstrap class blue color

from flaskblog import routes

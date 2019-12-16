from flaskblog import db, login_manager
from datetime import datetime
from flaskblog import login_manager
from flask_login import UserMixin

#a decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#here the table name will be automatically user
#we call also define our own table name
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)  #here P is capital coz it is refering the Post class

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

#here the table name will be automatically post
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)  #here the u is smaller coz we are accesing column from table

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

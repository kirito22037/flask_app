from flask_wtf import FlaskForm #for forms inheritance
from flask_wtf.file import FileField, FileAllowed  #for files
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField #for forms field
from wtforms.validators import DataRequired ,Length ,Email ,EqualTo ,ValidationError #for form field validators
from flaskblog.model import User
from flask_login import current_user

class RegistrationForm(FlaskForm): #inherit FlaskForm class
    username=StringField('Useraname',
                        validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')  #boolean value

    #when did these function are called ??
    #?????????????????
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first() #finding the username from table
        if user:
            raise ValidationError('That username is taken. Please choose a different user name !')

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first() #finding the username from table
        if email:
            raise ValidationError('That email is taken. Please choose a different email !')


class LoginForm(FlaskForm): #inherit FlaskForm class
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')     #boolean value


class UpdateAccountForm(FlaskForm): #inherit FlaskForm class
    username=StringField('Useraname',
                        validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
    picture=FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit=SubmitField('Update')  #boolean value

    #when did these function are called ??
    #?????????????????
    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first() #check whether the name already exist
            if user:
                raise ValidationError('That username is taken. Please choose a different user name !')

    def validate_email(self,email):
        if email.data != current_user.email:
            email=User.query.filter_by(email=email.data).first() #finding the username from table
            if email:
                raise ValidationError('That email is taken. Please choose a different email !')


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    submit=SubmitField('Post')

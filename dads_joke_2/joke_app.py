from flask import Flask,request
import requests
from flask import render_template,url_for
from random import choice

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired ,Length ,Email ,EqualTo ,ValidationError #for form field validators

from flask_bcrypt import Bcrypt
import sys 

app=Flask(__name__)
app.config['SECRET_KEY']='515ca6823d291bbb1108a59da2e7a3e2' #for CSRF
bcrypt=Bcrypt(app)


class searchform(FlaskForm):
    searchfield=StringField('Search',validators=[DataRequired(),Length(min=2,max=10)])
    submit=SubmitField('search')


def show_joke(user_input):
    url="https://icanhazdadjoke.com/search"
    print(user_input,file=sys.stderr)
    obj1=requests.get(url,headers={"Accept":"application/json"},params={"term":user_input})
    print(obj1.json(), file=sys.stderr)
    jokes_collection=obj1.json()['results']  # a list of jokes with key id and joke
    total_jokes=obj1.json()['total_jokes']
    joke=choice(jokes_collection)['joke']

    return joke,total_jokes


@app.route("/",methods=['GET','POST'])
#@app.route("/home",methods=['GET','POST'])
def home():
    form=searchform(request.form)  #instance of form class

    if form.validate() and request.method=='POST':
        joke,total_jokes=show_joke(form.searchfield.data)
        return render_template('home.html',title='home',form=form,joke=joke,total_jokes=total_jokes)
    
    else:
        return render_template('home.html',title='home',form=form)


if __name__=='__main__':
    app.run(debug=True)

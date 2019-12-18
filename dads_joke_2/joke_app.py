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

#this class will be form in our webpage and the class variable will be field in our webpage 
class searchform(FlaskForm):
    searchfield=StringField('Search',validators=[DataRequired(),Length(min=2,max=10)])  #input keyword
    submit=SubmitField('search')                                                        #submit button

#--------------------------------function starts--------------------------------------
def show_joke(user_input):
    url="https://icanhazdadjoke.com/search"
    print(user_input,file=sys.stderr)         #to check if input is fetched or not
    obj1=requests.get(url,headers={"Accept":"application/json"},params={"term":user_input}) #sending requesst to dadsjoke for jokes
    print(obj1.json(), file=sys.stderr)   #printing the data in json(dictionary) format     
  
    total_jokes=obj1.json()['total_jokes']    #total number of joke on that topic 

    if total_jokes==0:
        joke='NO JOKE RELATED TO THAT TOPIC FOUND!!'

    elif obj1.json()['status']!=200:
        joke="ERROR 404! CLIENT SIDE PROBLEM !"

    else:
        jokes_collection=obj1.json()['results']  # a list of jokes with key id and joke
        total_jokes=obj1.json()['total_jokes']
        joke=choice(jokes_collection)['joke']
    
    return joke,total_jokes

#----------------------------------function finish-------------------------------------

@app.route("/",methods=['GET','POST'])
#@app.route("/home",methods=['GET','POST'])
def home():
    form=searchform(request.form)  #instance of form class which can be used to send request(get,post)

    if form.validate() and request.method=='POST':      #when the form get submitted
        joke,total_jokes=show_joke(form.searchfield.data)  #function to search joke using api
        return render_template('home.html',title='home',form=form,joke=joke,total_jokes=total_jokes)
    
    else:
        return render_template('home.html',title='home',form=form)


if __name__=='__main__':
    app.run(debug=True)

from flask import Flask
import requests
from flask import render_template,url_for

app=Flask(__name__)
url="https://icanhazdadjoke.com/"

def show_jokes():
    response=requests.get(url, headers={"Accept":"application/json"})
    joke=response.json()
    return joke


@app.route("/")
@app.route("/home")
def home():
    joke=show_jokes()
    return render_template('home.html',title='home',joke_obj=joke)


if __name__=='__main__':
    app.run(debug=True)

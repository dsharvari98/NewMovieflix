from flask import Flask, render_template, session, redirect
from functools import wraps

import pymongo



app = Flask(__name__)
app.secret_key = 'movieflix'

client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

from user.models import User

@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout/')
def signout():
    return User().signout()

@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')



if __name__ == "__main__":
    app.run(debug=True)
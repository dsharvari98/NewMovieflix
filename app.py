from flask import Flask, render_template, session, redirect, request
from functools import wraps
from flask_mail import Mail
import pymongo



app = Flask(__name__)
app.secret_key = 'movieflix'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=False,
    MAIL_USERNAME='dpradnya757@gmail.com',
    MAIL_PASSWORD='Pradnu@59'
)
mail = Mail(app)

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

@app.route('/forget_pass/', methods=['POST'])
def forPass():
    return User().forget_password()

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
    return render_template('login.html')

@app.route('/signup/')
def signup_form():
    return render_template("register.html")

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")





if __name__ == "__main__":
    app.run(debug=True)
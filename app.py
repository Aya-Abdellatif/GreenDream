from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from helpers import *
from templateInfo import styles

cred = credentials.Certificate('green-dream-56ce5-firebase-adminsdk-33z10-b31fb21b8e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://green-dream-56ce5-default-rtdb.europe-west1.firebasedatabase.app/'
})


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def order_add(user, **kwargs):
    ref = db.reference(f'User/{user}/orders')
    ref.update({
        get_id(session["user_id"]): kwargs
    })



@app.after_request
def after_request(response):
    """No Cache"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'GET':
        return render_template("Login.html")
    else:
        user = db.reference(f'User/{request.form.get("number")}')
        f = request.form

        if None in [f.get('number'), f.get('password')] or '' in [f.get('number'), f.get('password')]:
            return error_message()
        print(f.get('number'), f.get('password'))
        if user.get() is None:
            return error_message("User does not exist or password is invalid")
        
        if request.form.get("password") != user.get()["password"]:
            return error_message("User does not exist or password is invalid")
        

        
        
        session['user_id'] = request.form.get("number")
        return redirect('/')


    
@app.route('/')
def index():
    try:
        session["user_id"]
        print('logged')
        ref = db.reference(f"User/{session['user_id']}")
        return render_template("dash.html", gender=True if ref.get()['gender'] == 'M' else False)
    except:
        return render_template("indx.html", log=False)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("registration.html")
    else:
        f = request.form
        if None in [f.get(attribute) for attribute in ["firstname", "lastname", "password", "firstname", "code", "email", "inlineRadioOptions", "address", "number"]]:
            return error_message()
        user = request.form.get('number')
        if db.reference(f"User/{user}").get() is not None:
            return error_message('User already exists with this phhone number :(')
        """Create User"""
        ref = db.reference('User')
        ref.update({
            request.form.get('number'):
            {
                'fname': request.form.get('firstname'),
                'lname': request.form.get('lastname'),
                'password': request.form.get('password'),
                'phonecode': request.form.get('code'),
                'email': request.form.get('email'),
                'gender': 'M' if request.form.get('inlineRadioOptions') == "option2" else 'F',
                'address': request.form.get('address'),
                'type': 'O' if request.form.get('inlineRadioOptions') == "option2" else 'U',
                'orders': {}
            }
        })

        session["user_id"] = request.form.get("number")

        return redirect('/')
    


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        ref = db.reference(f'User/{session["user_id"]}').get()
        return render_template('profile.html', ref=ref, gender=True if ref['gender'] == 'M' else False, number=session["user_id"])
    else:
        ref = db.reference(f'User/{session["user_id"]}')
        ref.update({
                'fname': request.form.get('firstname'),
                'lname': request.form.get('lastname'),
                'email': request.form.get('email'),
                'address': request.form.get('address')
        })
        return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/neworder', methods=["GET", "POST"])
def neworder():
    if request.method == 'GET':
        return render_template("cart.html")
    else:
        quantity = request.form.get('quantity')
        type = request.form.get('type')
        address = request.form.get('address')
        name = request.form.get('name')
        objname = request.form.get('objname')
        order_add(session["user_id"], quantity=quantity, type=type, address=address, name=name, objname=objname)
        return redirect('/')




"""
@app.route('/reset', methods=["GET", "POST"])
@login_required
def reset():
    old = request.form.get('old')
    new = request.form.get('new')

    if None in [old, new]:
        return error_message()
    
    user = db.reference(f'User/{session["user_id"]}')
    if user.get()["password"] != old:
        return error_message("Old password is incorrect")
    
    user.update({
        'password': new
    })

    return redirect('/')
"""
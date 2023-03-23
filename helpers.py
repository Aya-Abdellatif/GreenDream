from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def error_message(msg1="Something went wrong :(", msg2="Try again later.."):
    return render_template("error.html", msg1=msg1, msg2=msg2)



def get_id(phonenumber):
    now = datetime.now()
    return phonenumber + 'X' + now.strftime("%j%H%M%S")




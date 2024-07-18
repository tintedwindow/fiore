from flask import redirect, render_template, session
from functools import wraps
import random
import re
from uuid import uuid4
import os

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def allowed_file_type(filename):
    """Check for allowed file extensions"""
    # first checks file has an extension via .
    # and then splits the extension and checks the extension is in the following set
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'jfif', 'gif', 'webp'}

def street_link():
    """Returns a random google street view embed along with place name"""
    embed_views =[
        ["Arezzo", "https://www.google.com/maps/embed?pb=!4v1717524881466!6m8!1m7!1s4m0s7Uae-8vVJzPJSj_HJg!2m2!1d43.46736676185345!2d11.88359854501204!3f308.6546291458899!4f5.540173243496838!5f0.4000000000000002"],
        ["Liguria", "https://www.google.com/maps/embed?pb=!4v1717525460314!6m8!1m7!1s82T9AG1NMKvRgpd9nze1Yg!2m2!1d44.13640524169838!2d9.765037289350103!3f9.562905459513086!4f-9.76672118128117!5f0.7820865974627469"]
        ["Cortona", "https://www.google.com/maps/embed?pb=!4v1721327298805!6m8!1m7!1svJxShiP71Z82mHEmv3lxQA!2m2!1d43.27525568477115!2d11.98785088016457!3f177.77!4f-8.379999999999995!5f0.7820865974627469"]
    ]

    return random.choice(embed_views)

def apology(message, code=400):
    """ Renders an apology page with a street view"""
    return render_template("apology.html", message=message, place_info=street_link()), code


def valid_username(username):
    if not 4 <= len(username) <= 20:
        return "Username must be between 4 and 20 characters"
    elif not re.match(r"^[a-zA-Z0-9_]*$", username):
        return "Username can only contain letters, numbers, and underscores"
    else:
        return 200 # a bit of an easter egg to http ok :)
    

def valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters"
    elif not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    elif not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    elif not re.search(r"[0-9]", password):
        return "Password must contain at least one digit"
    elif not re.search(r"[!@#$%^&*]", password):
        return "Password must contain at least one special character"
    else:
        return 200
    
def format_description(description):
    """Formats the description of the user if they have one else returns none"""
    if not description:
        return None
    
    description_list = description.split(".")
    
    if len(description_list[0]) > 40:
        return description_list[0][:40] + "..."

    if len(description_list) > 1:
        if description_list[1] != '':
            return description_list[0] + "..."
        else:
            return description_list[0] + "."
    else:
        return description_list[0]
    
def generate_filename(filename, year, month, day):
    """ formats the file name to a unique identifier with date at end """

    _, ext = os.path.splitext(filename)
    year = str(year).zfill(4)
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    return (year + month + day + "-" + str(uuid4()) + ext)

    
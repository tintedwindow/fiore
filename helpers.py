from flask import redirect, render_template, session
from functools import wraps
import random

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
    ]

    return random.choice(embed_views)
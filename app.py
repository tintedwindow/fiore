import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import logging

from helpers import login_required


# Configuring the application
app = Flask(__name__)

# Makes changes to html/css on page reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fiore.db")

# Echoes what the sql query is executed in flask terminal
# https://cs50.readthedocs.io/libraries/cs50/python/#how-can-i-disable-logging-of-sql-statements
logging.getLogger("cs50").disabled = False

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via a GET -> Simply clicking from home screen
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    #User reached route via POST (by submitting the registation form)
    if request.method == "POST":
        username = request.form.get("username")
        # Ensure username was submitted and isn't taken
        print(username)
        if not username:
            return render_template("apology.html", message = "Username not submitted")
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return render_template("apology.html", message= "Username already taken")
        print(username + "1")
        password = request.form.get("password")
        password_c = request.form.get("confirmation")

        print(password, password_c)
        # Ensure passwords were submitted and both fields match
        if not password or not password_c:
            return render_template("apology.html", message = "Password not submitted")
        if password != password_c:
            return render_template("apology.html", message = "Passwords do not match")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        print(username)
        return redirect("/login")
    else:
        print("Helloo")
        db.execute("SELECT * FROM users")
        return render_template("register.html")

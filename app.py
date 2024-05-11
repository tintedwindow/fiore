import os

import calendar
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from PIL import Image
from werkzeug.utils import secure_filename

from helpers import login_required, allowed_file_type


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



@app.route('/upload', methods=["POST"])
@login_required
def upload():
    
    # this part of post will handle the image that the user uploads
        # take the image
            # check for if the image is actually an image jpeg/png ...
            # associate a random string with that image
                # check that random string isn't associated with a previous image (very rare to NO chance, but still check)
            # store the image in a folder for images
            
    # check for post request requirements
    if 'file' not in request.files:
        return jsonify({'error': 'No file added'}), 400
    if not request.form.get("date"):
        return jsonify({'error': 'No date added'}), 400
        
    file = request.files['file']
    description = request.form.get('description', '').strip() # defult to an empty string if no description provided
    if description == '':
        description = None

    # Check if the user has actually selected a file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file_type(file.filename):
        # Read the file stream
        
        file_stream = file.stream
        file_stream.seek(0) # going to beginning of the file stream

        try:
            # load image from stream
            img = Image.open(file_stream)
            img.verify() # verify it's a valid image

            # If image is valid, get a file name and save it permanently

            filename = secure_filename(file.filename)
            file_stream.seek(0) # go back to beginning of file stream
            img = Image.open(file_stream)
            save_path = os.path.join('./uploads', filename)
            img.save(save_path)

            day = int(request.form.get('date'))
            month = session["month"]
            year = session["year"]
            image_date = datetime(year, month, day)
            print(image_date)

            db.execute("INSERT INTO images (user_id, path, image_date, description) VALUES (?, ?, ?, ?)", session['user_id'], save_path, image_date, description)

            return jsonify({'message': 'File successfully uploaded', 'filename': filename}), 200
        except Exception as e:
            return jsonify({'error': 'Invalid image file: {}'.format(e)}), 400
    else:
        return jsonify({'error': 'Allowed file types are .png .jpg .jpeg .gif .webp'}), 400


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    if request.method == "POST":
        print(session["month"] , session["year"])
        # do the calculation per value and display the form
        month_updater = int(request.form.get("month_updater"))
        print(month_updater)


        if ((session["month"] + month_updater) > 12):
            session["year"] = session["year"] + 1
            session["month"] = 1

        elif(((session["month"] + month_updater) < 1)):
            session["year"] = session["year"] - 1
            session["month"] = 12

        else:
            session["month"] = session["month"] + month_updater

        # get new values for templating
        month_name = calendar.month_name[session["month"]]
        month = session["month"]
        year = session["year"]
        print(month, year)

        current_cal = calendar.monthcalendar(year, session["month"])

        user = db.execute(
            "SELECT id, username FROM users WHERE id = ?", session["user_id"]
        )

        images = db.execute("SELECT path, image_date, description FROM images WHERE user_id = ? AND strftime('%Y-%m', image_date) = ?",
                            session["user_id"], f"{year}-{month:02}")

        images_by_day = {datetime.strptime(img['image_date'], '%Y-%m-%d %H:%M:%S').day: {'image_path': img['path'], 'description': img['description']} for img in images}
        return render_template("home_new.html", name = user[0]["username"], calendar=current_cal, month_name=month_name, year=year, images_by_day=images_by_day)
    

    else:
        # seeds with the current month integer
        session["month"] = datetime.now().month
        # same with year
        session["year"] = datetime.now().year

        #get current month name dynamically
        month_name = calendar.month_name[session["month"]]
        month = session["month"]
        year = session["year"]

        user = db.execute(
            "SELECT id, username FROM users WHERE id = ?", session["user_id"]
        )

        images = db.execute("SELECT path, image_date, description FROM images WHERE user_id = ? AND strftime('%Y-%m', image_date) = ?",
                            session["user_id"], f"{year}-{month:02}")

        images_by_day = {datetime.strptime(img['image_date'], '%Y-%m-%d %H:%M:%S').day: {'image_path': img['path'], 'description': img['description']} for img in images}

        current_cal = calendar.monthcalendar(year, session["month"])
        return render_template("home_new.html", name = user[0]["username"], calendar=current_cal, month_name=month_name, year=year, images_by_day=images_by_day)




@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting login form)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", message="Must provide username"), 403
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", message = "Must provide password"), 403
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("apology.html", message = "Invalid username"), 403
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message = "Incorrect password"), 403
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")
        
    # User reached route via a GET -> Simply clicking from home screen
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

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

import os
import sys
import calendar
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_from_directory, url_for, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from PIL import Image
from werkzeug.utils import secure_filename

from helpers import login_required, allowed_file_type, street_link, apology, valid_username, valid_password, format_description, generate_filename


# Configuring the application
app = Flask(__name__)

# Makes changes to html/css on page reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
try:
    db = SQL("sqlite:///fiore.db")
except RuntimeError:
    print("Consider running the following command first:")
    print("python3 schema.py")
    sys.exit()
    
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

@app.route('/<path:filename>/')
@app.route('/<path:filename>/<int:thumbnail>')
def uploaded_file(filename, thumbnail=None):

    #autheticate the image
    images = db.execute("SELECT filename FROM images WHERE user_id = ?;", session["user_id"])
    if not filename in [image['filename'] for image in images]:
       return apology("Is that your book, Potter?", 404)
    
    if thumbnail: 
        image_path = os.path.join('./uploads/thumbnails', 'thumb-' + filename)
    else:
        image_path = os.path.join('./uploads', filename)

    return send_from_directory(os.getcwd(), image_path)

@app.errorhandler(404)
def page_not_found(e):
    # this expects an argument in any case
    return apology("Are you really focusing your mind on where to apparate, Potter?", 404)

@app.errorhandler(500)
def internal_error(e):
    return apology("Are you really trying to mix random potions, Potter?", 500)


@app.route('/delete-account', methods=["POST"])
@login_required
def delete_account():
    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({"success": False, "error": "Password field is empty"})

    # authenticate user
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    if not check_password_hash(rows[0]["hash"], password):
        return jsonify({"success": False, "error": "Incorrect password"})
    

    # get and delete all locally stored images
    filenames = db.execute("SELECT filename FROM images WHERE user_id = ?;", session["user_id"])

    for file in filenames:
        # delete from upload and thumbnail directories
        filename = file["filename"]
        os.remove(os.path.join('./uploads/thumbnails', 'thumb-' + filename))
        os.remove(os.path.join('./uploads', filename))

    # delete the user; user deletion cascades to entry deletion via constraint
    db.execute("DELETE FROM users WHERE id = ?;", session["user_id"])

    # Forget user_id and return fetch
    session.clear()
    return jsonify({"success": True})


@app.route('/entry-scroll', methods=["GET"])
def entry_scroll():
    # retrieve the last or the next entry of the user
    try:
        updater = int(request.args.get("updater"))
        day = int(request.args.get("d"))
        month = int(request.args.get("m"))
        year = int(request.args.get("y"))
    except ValueError:
        return apology("Are you sure you are using the correct spells, Potter?", 403)
    
    if updater == -1:
        date_info = db.execute("SELECT image_date FROM images WHERE user_id = ? AND DATE(image_date) < ? ORDER BY image_date DESC LIMIT 1;",
                            session["user_id"], f"{year}-{month:02}-{day:02}")
    else:
        date_info = db.execute("SELECT image_date FROM images WHERE user_id = ? AND DATE(image_date) > ? ORDER BY image_date ASC LIMIT 1;",
                        session["user_id"], f"{year}-{month:02}-{day:02}")
    
    if date_info:
        date = datetime.strptime(date_info[0]["image_date"], '%Y-%m-%d %H:%M:%S')
        return redirect(url_for('day_info', d=date.day, m=date.month, y=date.year))
    else:
        return redirect("/home")

@app.route('/calendar-scroll', methods=["GET"])
def calendar_scroll():
    try:
        updater = int(request.args.get("updater"))
        month = int(request.args.get("m"))
        year = int(request.args.get("y"))
    except ValueError:
        return apology("Are you sure you are using the correct spells, Potter?", 403)
    
    if ((month + updater) > 12):
        year = year + 1
        month = 1
    elif(((month + updater) < 1)):
        year = year - 1
        month = 12
    else:
        month = month + updater

    return redirect(url_for('home', m=month, y=year))

@app.route("/delete", methods=["POST"])
def delete():

    if not (request.form.get("d") and request.form.get("m") and request.form.get("y")):
        return apology("Are you sure you are casting the vanishing spell correctly, Potter?", 403)
    
    try:
        day = int(request.form.get("d"))
        month = int(request.form.get("m"))
        year = int(request.form.get("y"))
    except ValueError:
        return apology("Are you sure you are using the correct spells, Potter?", 403)

    image_info = db.execute("SELECT image_id, filename FROM images WHERE user_id = ? AND strftime('%Y-%m-%d', image_date) = ?",
                        session["user_id"], f"{year}-{month:02}-{day:02}")
    
    if(image_info):

        # delete from upload and thumbnail directories
        filename = image_info[0]["filename"]
        os.remove(os.path.join('./uploads/thumbnails', 'thumb-' + filename))
        os.remove(os.path.join('./uploads', filename))

        #delete entry from database
        db.execute("DELETE FROM images WHERE user_id = ? AND strftime('%Y-%m-%d', image_date) = ?",
                            session["user_id"], f"{year}-{month:02}-{day:02}")
        
        flash('Deleted entry for ' + str(day) + " " + calendar.month_name[month] + " " + str(year))
        return redirect(url_for('home', m=month, y=year))

    else:
        return apology("First you need something to practice vanishing on, Potter.", 403)      


@app.route("/italy")
def italy():
    return render_template("apology.html", italy=True, place_info=street_link())


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/resources')
def resources():
    return render_template("resources.html", places=street_link(return_all=True))

    return apology("These are the books you have to consult, Potter!")

@app.route('/acknowledgements')
def acknowledgements():
    return render_template("acknowledgements.html")
    # return apology("You can thank me for hepling you in Hogwarts, Potter!")


@app.route('/profile')
@login_required
def profile():
    
    creation_date = db.execute("SELECT creation_date FROM users WHERE id = ?", session["user_id"])
    creation_date = datetime.strptime(creation_date[0]["creation_date"], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
    description_count = db.execute("SELECT COUNT(description) as descriptions FROM images WHERE user_id = ?", session["user_id"])
    description_count = description_count[0]["descriptions"]
    entry_count = db.execute("SELECT COUNT(image_date) as total_dates FROM images WHERE user_id = ?", session["user_id"])
    entry_count = entry_count[0]["total_dates"]

    entries = db.execute("SELECT image_date, description, upload_date FROM images WHERE user_id = ?", session["user_id"])

    entries_by_day= {datetime.strptime(entry['image_date'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'): {'upload_date': datetime.strptime(entry['upload_date'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'), 'description': format_description(entry['description'])} for entry in entries}

    return render_template("profile.html", entries_by_day=entries_by_day, creation_date=creation_date, description_count=description_count, entry_count=entry_count)

@app.route('/day-info', methods=["POST", "GET"])
@login_required
def day_info():
    if request.method == "GET":
        print(request.args.get("d"))
        print(request.args.get("m"))
        print(request.args.get("y"))

        if not (request.args.get("d") and request.args.get("m") and request.args.get("y")):
            return apology("Are you sure you have all the books, Potter?", 403)
        
        day = int(request.args.get("d"))
        month = int(request.args.get("m"))
        year = int(request.args.get("y"))
        month_name = calendar.month_name[month]

    
        day_details = db.execute("SELECT filename, description FROM images WHERE user_id = ? AND strftime('%Y-%m-%d', image_date) = ?",
                        session["user_id"], f"{year}-{month:02}-{day:02}")
        
        if day_details:
            # If there is an image for the selected date, render the image page
            return render_template('day_info.html', name=session["user_name"], day_details=day_details, day = day, month=month, month_name=month_name, year=year)
        else:
            # If there is no image for the selected date, return an error message
            return apology("Are you sure you are on the right date, Potter?", 403)
    else :
        return apology("Are you roaming around unknown request corridors, Potter?", 403)

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
    if not request.form.get("month"):
        return jsonify({'error': 'No month added'}), 400
    if not request.form.get("year"):
        return jsonify({'error': 'No year added'}), 400
            
    file = request.files['file']
    description = request.form.get('description', '').strip() # defult to an empty string if no description provided
    if description == '':
        description = None

    # Check if the user has actually selected a file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        day = int(request.form.get('date'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
    except ValueError:
        return apology("Are you sure you are using the correct spells, Potter?", 403)
    
    if file and allowed_file_type(file.filename):
        # Read the file stream
        
        file_stream = file.stream
        file_stream.seek(0) # going to beginning of the file stream

        try:
            # load image from stream
            img = Image.open(file_stream)
            img.verify() # verify it's a valid image

            # If image is valid, get a file name and save it permanently
            filename = secure_filename(generate_filename(file.filename, year, month, day))
            file_stream.seek(0) # go back to beginning of file stream
            img = Image.open(file_stream)
            save_path = os.path.join('./uploads', filename)
            img.save(save_path)
            #saves a low rez thumbnail
            img.thumbnail((800, 800)) #resizes the image to max 800 x 800 pixels
            thumb_path = os.path.join('./uploads/thumbnails', 'thumb-' + filename)
            img.save(thumb_path)


            image_date = datetime(year, month, day)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute("INSERT INTO images (user_id, filename, image_date, description, upload_date) VALUES (?, ?, ?, ?, ?)", session['user_id'], filename, image_date, description, current_date)
        
            return jsonify({'message': 'File successfully uploaded', 'filename': filename, 'day' : day, 'description': description.split(".")[0] + "..." if description else None, 'filename': filename }), 200
        except Exception as e:
            return jsonify({'error': 'Invalid image file: {}'.format(e)}), 400
    else:
        return jsonify({'error': 'Allowed file types are .png .jpg .jpeg .gif .webp'}), 400


@app.route("/home", methods=["GET"])
@login_required
def home():
    if request.method == "GET":
        print(request.args.get("m"))
        print(request.args.get("y"))

        if(request.args.get("m") and request.args.get("y")):
                               
            # do the calculation per value and display the form
            try:
                month = int(request.args.get("m"))
                year = int(request.args.get("y"))
            except ValueError:
                return apology("Are you sure you are using the correct spells, Potter?", 403)
            
            if (month < 1 or month > 12 or year >= 2100):
                return apology("Are you trying to break a school rule and go out of bounds, Potter?", 403)
            
            # get new values for templating
            month_name = calendar.month_name[month]

            current_cal = calendar.monthcalendar(year, month)

            images = db.execute("SELECT filename, image_date, description FROM images WHERE user_id = ? AND strftime('%Y-%m', image_date) = ?",
                                session["user_id"], f"{year}-{month:02}")

            images_by_day = {datetime.strptime(img['image_date'], '%Y-%m-%d %H:%M:%S').day: {'filename': img['filename'], 'description': format_description(img['description'])} for img in images}

            # checks if redirected by delete
            message = get_flashed_messages()
            if message:
                message = message[0]

            return render_template("home_new.html", name = session["user_name"], calendar=current_cal, month_name=month_name, month=month, year=year, images_by_day=images_by_day, message=message)

        #if visited with an empty url i.e. simply coming to home
        else:
            # seeds with the current month integer
            month = datetime.now().month
            # same with year
            year = datetime.now().year

            #get current month name dynamically
            month_name = calendar.month_name[month]

            images = db.execute("SELECT filename, image_date, description FROM images WHERE user_id = ? AND strftime('%Y-%m', image_date) = ?",
                                session["user_id"], f"{year}-{month:02}")

            images_by_day = {datetime.strptime(img['image_date'], '%Y-%m-%d %H:%M:%S').day: {'filename': img['filename'], 'description': img['description'].split(".")[0] + "..."  if img['description'] else None} for img in images}

            current_cal = calendar.monthcalendar(year, month)
            return render_template("home_new.html", name = session["user_name"], calendar=current_cal, month_name=month_name, month=month, year=year, images_by_day=images_by_day)


@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting login form)
    if request.method == "POST":            
        # Forget any user_id
        session.clear()
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        #400 status code for blank inputs suggested by dbb, as it indicates bad request due to client error
        if not username:
            return jsonify({"error": "Username cannot be blank"}), 400 
        if not password:
            return jsonify({"error": "Password cannot be blank"}), 400
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return jsonify({"error": "Username not found"}), 401
        elif not check_password_hash(rows[0]["hash"], password):
            return jsonify({"error": "Incorrect password"}), 401
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = username

        # Redirect user to home page
        return jsonify({"message": "Login successful"}), 200
        
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
        # Forget any user_id
        session.clear()
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        password_c = data.get('passwordConfirm')


        if not username:
            return jsonify({"error": "Username cannot be blank"}), 400
        if not password or not password_c:
            return jsonify({"error": "Password cannot be blank"}), 400
        if password != password_c:
            return jsonify({"error": "Passwords do not match"}), 400
        
        # Check if username already exists
        rows = db.execute(
            "SELECT id FROM users WHERE username = ?", username
        )
        if len(rows) != 0:
            return jsonify({"error": "Username already taken"}), 401
           
        #validate the username and password 
        if valid_username(username) != 200:
            return jsonify({"error": valid_username(username)}), 400 
        if valid_password(password) != 200: 
            return jsonify({"error": valid_password(password)}), 400 
            
        # proceed with storing user
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO users (username, hash, creation_date) VALUES (?, ?, ?)", username, generate_password_hash(password), current_date)
        
        return jsonify({"message": "Registration successful"}), 200
    
    else:
        print("Helloo")
        db.execute("SELECT * FROM users")
        return render_template("register.html")

# Street Style: fashion website

import os
import json
from datetime import datetime
import calendar
from collections import Counter

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, dateString

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fashion.db")

# TO DO: On line 29 change the number between workspaces and WEBSITE with your codespace number
app.config["IMAGE_UPLOADS"] = "/workspaces/#/WEBSITE/static/img/uploads"
imagefilepath = "/static/img/uploads/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPEG", "JPG", "GIF"]

# Validation for image extensions
def allowed_image(filename):
    """Determine image validity"""

    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/")
@login_required
def index():
    """Shows home page with profile info"""

    profile = db.execute("SELECT * from profile WHERE id = ?", session["user_id"])
    birthString = dateString(profile[0]['birthday'])

    # Use N/A image if no image
    if profile[0]['filepath'] == 'N/A':
        profile[0]['filepath'] = "/static/noImg.png"

    return render_template("index.html", profile=profile[0], birthString=birthString)

@app.route("/journal")
@login_required
def journal():
    """Shows user journal"""

    # Get user's journal entries
    entries = db.execute("SELECT date, title, subject, entry FROM journal WHERE user_id = ? ORDER BY date DESC", session["user_id"])

    # Convert dates from YYYY-MM-DD
    for entry in range(len(entries)):
        entries[entry]['date'] = dateString(entries[entry]['date'])

    return render_template("journal.html", entries=entries)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check for username
        if not request.form.get("username"):
            flash('Must provide username')
            return render_template("login.html")

        # Check for password
        elif not request.form.get("password"):
            flash('Must provide password')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check username usernames and password good
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid username or password')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    """Register new user"""

    if request.method == "POST":

        # Form's inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for username
        if not username:
            flash("Must provide username")
            return redirect("/register")

        # Check for password
        if not password:
            flash("Must provide password")
            return redirect("/register")

        # Check for confirmation
        if not confirmation:
            flash("Must provide confirmation")
            return redirect("/register")

        # Check password and confirmation match
        elif password != confirmation:
            flash("Password must match")
            return redirect("/register")

        # Check password strength: at least 8 characters
        if len(password) < 8:
            flash("Password must be at least 8 characters")
            return redirect("/register")

        # Password needs one lower, one capital, one symbol, one number
        lower, capital, symbol, number = False, False, False, False

        for letter in password:
            if letter.islower():
                lower = True
            if letter.isupper():
                capital = True
            if not letter.isalnum():
                symbol = True
            if letter.isdigit():
                number = True

        if not (lower and capital and symbol and number):
            flash("Password is too weak: needs one uppercase, lowercase, symbol, and number")
            return redirect("/register")

        # Try to insert user into database and redirect to login
        try:
            # Any login has same id for users and profile table
            id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
            db.execute("INSERT INTO profile (id) VALUES(?)", id)

        # Check if username already exists
        except ValueError:
            flash("User already exists")
            return redirect("/register")

        session["user_id"] = id
        return render_template("profile.html")

    # Get method displays registration form
    else:
        return render_template("register.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    """Register new user"""

    if request.method == "POST":

        name = request.form.get("name")
        birthday = request.form.get("birthday")
        hometown = request.form.get("hometown")
        brand = request.form.get("brand")
        image = request.files["image"]

        # Check if name filled out
        if not name:
            flash("Must submit a name")
            return redirect("/profile")

        # Check if birthday filled out
        if not birthday:
            flash("Must submit a birthday")
            return redirect("/profile")

        # Make sure image has a name
        if image.filename == "":
            flash ("Missing image")
            return redirect("/profile")

        # Make sure uploaded file is an image
        if not allowed_image(image.filename):
            flash ("Upload valid image file")
            return redirect("/profile")

        # Make sure image name has no spaces
        if ' ' in image.filename:
            flash("Image name must not have any spaces")
            return redirect("/profile")

        # Check if hometown filled out
        if not hometown:
            flash("Must submit a hometown")
            return redirect("/profile")

        # Check if brand filled out
        if not brand:
            flash("Must submit a brand")
            return redirect("/profile")

        # Save image in specified path
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

        db.execute("UPDATE profile SET name = ?, hometown = ?, birthday = ?, picture = ?, filepath = ? WHERE id = ?", name, hometown, birthday, image.filename, imagefilepath + image.filename, session["user_id"])

        return redirect("/")

    # Get method displays registration form
    else:
        return render_template("profile.html")

@app.route("/journal_post", methods=["GET", "POST"])
@login_required
def journal_post():
    """Create new journal entry"""

    if request.method == "POST":

        date = request.form.get("date")
        title = request.form.get("title")
        subject = request.form.get("subject")
        entry = request.form.get("entry")

        # Check for date
        if not date:
            flash("Missing date")
            return redirect("/journal_post")

        # Check for title
        if not title:
            flash("Missing title")
            return redirect("/journal_post")

        # Check for subject
        if not subject:
            flash("Missing subject")
            return redirect("/journal_post")

        # Check for entry
        if not entry:
            flash("Missing entry")
            return redirect("/journal_post")

        # Enter new entry into database
        db.execute("INSERT INTO journal (user_id, date, title, subject, entry) VALUES (?, ?, ?, ?, ?)", session["user_id"], date, title, subject, entry);

        # Redirect user to old blog posts
        return redirect("/journal")

    else:
        return render_template("journal_post.html")

@app.route("/shopping_log", methods=["GET", "POST"])
def shopping_log():
    """User can log clothing"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Save the form data in variables
        date = request.form.get("date")
        article = request.form.get("article")
        brand = request.form.get("brand")
        link = request.form.get("link")

        # Check for date
        if not date:
            flash("Missing date")
            return redirect("/shopping_log")

        # Make sure image has a name
        image = request.files["image"]
        if image.filename == "":
            flash("Missing image")
            return redirect("/shopping_log")

        # Make sure uploaded file is an image
        if not allowed_image(image.filename):
            flash("Upload valid image file")
            return redirect("/shopping_log")

        # Make sure image name has no spaces
        if ' ' in image.filename:
            flash("Image name must not have any spaces")
            return redirect("/shopping_log")

        # Check for clothing type
        if not article:
            flash("Missing article")
            return redirect("/shopping_log")

        # Check for brand
        if not brand:
            flash("Missing brand")
            return redirect("/shopping_log")

        # Save image in specified path
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

        # Insert into table
        db.execute("INSERT INTO shopping_log (date, picture, filepath, article, brand, link, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", date, image.filename, imagefilepath + image.filename, article, brand, link, session["user_id"])

        # Show user fashion history
        return redirect("/shopping_log_history")

    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("shopping_log.html")

@app.route("/shopping_log_history", methods=["GET"])
def shopping_log_history():
    """Shows user clothes history"""

    shopping_log_history = db.execute("SELECT * FROM shopping_log WHERE user_id = ? ORDER BY date DESC", session["user_id"])

    # Convert dates from YYYY-MM-DD
    for entry in range(len(shopping_log_history)):
        shopping_log_history[entry]['date'] = dateString(shopping_log_history[entry]['date'])

    return render_template("shopping_log_history.html", shopping_log_history=shopping_log_history)

@app.route('/analytics')
def analytics():
    """Display data on user's clothing habits"""

    # Get article/brand and date
    userInfo = db.execute("SELECT article, brand FROM shopping_log WHERE user_id = ?", session["user_id"])
    dates = db.execute("SELECT date FROM shopping_log WHERE user_id = ? AND date LIKE ? ORDER BY date", session["user_id"], "%" + str(datetime.now().year) + "%")

    # Keep track of numbers
    articleDict = {'Accessory': 0, 'Hat': 0, 'Top': 0, 'Bottom': 0, 'Shoes': 0}

    brandCount = {}

    sortedBrands = {1: ["Top Brand", 0],
                    2: ["2nd Top Brand", 0],
                    3: ["3rd Top Brand", 0],
                    4: ["4th Top Brand", 0],
                    5: ["5th Top Brand", 0]}

    dateCount = {'January': 0, 'February': 0, 'March': 0, 'April': 0,
                'May': 0, 'June': 0, 'July': 0, 'August': 0,
                'September': 0, 'October': 0, 'November': 0, 'December': 0}

    # Go through logged articles and update counts
    for i in range(len(userInfo)):
        articleDict[userInfo[i]['article']] += 1

    # Go through logged brands
    for i in range(len(userInfo)):

        # If not there, addd new key/value to brandCount
        if brandCount.get(userInfo[i]['brand']) == None:
            brandCount[userInfo[i]['brand']] = 1

        # The brand is already a key so update count
        else:
            brandCount[userInfo[i]['brand']] += 1

    # Get keys of the top five brands
    topKeys = list(dict(Counter(brandCount).most_common()[0:5]).keys())

    # Update dictionary for top five key-value
    for i in range(len(topKeys)):
        sortedBrands[i+1] = [topKeys[i], brandCount[topKeys[i]]]

    # Count posts per month
    for i in range(len(dates)):
        # Determine month and update count
        month = calendar.month_name[int(dates[i]['date'].split("-")[1])]
        dateCount[month] += 1

    return render_template("analytics.html", dateCount=dateCount, sortedBrands=sortedBrands, articleDict=articleDict)

@app.route('/randomizer', methods=["GET"])
def randomizer():

    # Get a list of dictionaries for each article type
    py_accessories = db.execute("SELECT filepath, brand FROM shopping_log WHERE user_id = ? AND article = ?", session["user_id"], "Accessory")
    py_hats = db.execute("SELECT filepath, brand FROM shopping_log WHERE user_id = ? AND article = ?", session["user_id"], "Hat")
    py_tops = db.execute("SELECT filepath, brand FROM shopping_log WHERE user_id = ? AND article = ?", session["user_id"], "Top")
    py_bottoms = db.execute("SELECT filepath, brand FROM shopping_log WHERE user_id = ? AND article = ?", session["user_id"], "Bottom")
    py_shoes = db.execute("SELECT filepath, brand FROM shopping_log WHERE user_id = ? AND article = ?", session["user_id"], "Shoes")

    return render_template("randomizer.html", accessories=json.dumps(py_accessories), hats=json.dumps(py_hats), tops=json.dumps(py_tops), bottoms=json.dumps(py_bottoms), shoes=json.dumps(py_shoes))

# OUR TABLES

"""
CREATE TABLE users
(   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE UNIQUE INDEX unique_username ON users (username);

CREATE TABLE profile
(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL DEFAULT "N/A",
    hometown TEXT NOT NULL DEFAULT "N/A",
    birthday TEXT NOT NULL DEFAULT "N/A",
    filepath TEXT NOT NULL DEFAULT "N/A",
    picture TEXT NOT NULL DEFAULT "N/A",
    FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE journal
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    entry TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE shopping_log
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    picture TEXT NOT NULL,
    filepath TEXT NOT NULL,
    article TEXT NOT NULL,
    brand TEXT NOT NULL,
    link TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""
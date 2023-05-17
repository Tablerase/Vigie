import os

# basics packages for flask site
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# external py addons
from helpers import apology, login_required

# tools
from datetime import datetime
import json

# api scrap data


# post
from post import tweet_create

# Configure application
app = Flask(__name__)

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///vigie.db")

'''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL
);'''
'''CREATE TABLE "post" (
	"id"	INTEGER,
	"content"	TEXT NOT NULL,
	"publish"	TEXT NOT NULL,
	"userid"	INTEGER,
	"date"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("userid") REFERENCES "users"("id")
);'''

# set time
# datetime object containing current date and time
now = datetime.now()  # now = 2022-12-27 10:09:20.430322
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # date and time = 27/12/2022 10:09:20
dates = now.strftime('%d/%m/%Y') # dd/mm/YY
times = now.strftime('%H:%M:%S') # H:M:S


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # get username
    userid = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", userid)
    username = username[0]["username"]
    
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
    """Register user"""
    # get register html form
    if request.method == "GET":
        return render_template("register.html")

    # add user to database
    elif request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Check if user already exist database for username
        regname = request.form.get("username")
        checkrow = db.execute("SELECT * FROM users WHERE username = ?", regname)
        if len(checkrow) > 0:
            return apology("user already exist")

        # confirmation password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("Mismatch between password and confirmation password")
        else:
            # Add user / password
            passwordh = generate_password_hash(password)  # hash password
            db.execute("INSERT INTO users(username, hash) VALUES(? , ?)", regname, passwordh)
            return redirect("/")


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    userid = session["user_id"]
    # get register html form
    if request.method == "GET":
        # gather db of past post for log userid
        return render_template("post.html")
    # post via form content
    elif request.method == "POST":
        # Get form data
        text = request.form.get("texttopost")
        if text == None:
            return apology("You must write a text to be publish")
        # Get sociales to post to
        tweet = request.form.get("tweet-form")
        insta = request.form.get("insta-form")
        # Check if sociales are select
        check = bool(tweet) + bool(insta)
        if check == False: 
            return apology("You must choose where to publish")
        else:
            # Post depending of social
            publish = {}
            if bool(tweet) == True:
                print(f"Tweet {tweet}")
                r = tweet_create(text)
                twitter_link = r['link']
                twitter_id = r['id']
                publish.update({'Twitter': twitter_id, 'link': twitter_link})
            if bool(insta) == True:
                print(f"Insta {insta}")
                publish.append('Instagram')

            # Database save
            publish_json = json.dumps(publish)
            db.execute("INSERT INTO post(content, publish, userid, date) VALUES (?, ?, ?, ?)", text, publish_json, userid, dt_string)
            print(dt_string, publish)

            return redirect("/post")


@app.route("/tweet/create", methods=["GET", "POST"])
@login_required
def tweet():
    return redirect("/post")
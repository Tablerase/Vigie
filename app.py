import os

# basics packages for flask site
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime
from helpers import apology, login_required

# api scrap data
from scrap import twitter_hashtag

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
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")

# set time
# datetime object containing current date and time
now = datetime.now()  # now = 2022-12-27 10:09:20.430322
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # date and time = 27/12/2022 10:09:20


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
        

@app.route("/tweet/<msg>")
@login_required
def tweet():
    
    
    return render_template("index.html")
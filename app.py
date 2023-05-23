
# basics packages for flask site
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# external py addons
from helpers import apology, login_required

# tools
from datetime import datetime
import json

# post
from post import tweet_create, reddit_create

# Configure application
app = Flask(__name__)

# Add some jinja functions
# zip allow to tuple and use multiple list in for loops
app.jinja_env.globals['zip'] = zip


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///vigie.db")

'''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL,
    api	TEXT,
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
        postdb = db.execute("SELECT content, publish, date FROM post WHERE userid= ? ORDER BY date DESC", userid)
        publish_list = []
        for row in postdb:
            publish_row = json.loads(row['publish'])
            publish_list.append(publish_row)
        return render_template("post.html", postdb= postdb, publish=publish_list)
    # post via form content
    elif request.method == "POST":
        # Get form data
        text = request.form.get("texttopost")
        if text == None:
            return apology("You must write a text to be publish")
        # Get sociales to post to
        tweet = request.form.get("tweet-form")
        reddit = request.form.get("reddit-form")
        # Check if sociales are select
        check = bool(tweet) + bool(reddit)
        if check == False: 
            return apology("You must choose where to publish")
        else:
            # Post depending of social
            publish = {'link':[]}
            if bool(tweet) == True:
                if len(text) > 280:
                    return apology("Content to long to be supported by Tweeter free API")
                else:
                    r = tweet_create(text, userid)
                    twitter_link = r['link']
                    twitter_id = r['id']
                    publish.update({'Twitter': twitter_id})
                    publish['link'].append(twitter_link)
            if bool(reddit) == True:
                reddit_title = request.form.get("content-title")
                if reddit_title == None:
                    return apology("You must add a title if you want to publish on Reddit")
                else:
                    reddit_result = reddit_create(text, reddit_title, userid)
                    reddit_id = reddit_result['id']
                    reddit_link = reddit_result['link']
                    publish.update({'Reddit':reddit_id, 'Title': reddit_title})
                    publish['link'].append(reddit_link)
                
            # Database save
            publish_json = json.dumps(publish)
            db.execute("INSERT INTO post(content, publish, userid, date) VALUES (?, ?, ?, ?)", text, publish_json, userid, dt_string)
            return redirect("/post")


@app.route("/api", methods=["GET", "POST"])
@login_required
def api():
    userid = session["user_id"]
    # get register html form
    if request.method == "GET":
        # Query the database to get user api
        apiencrypted = db.execute("SELECT api FROM users WHERE id= ?", userid)
        # if API infos is empty
        if apiencrypted[0]['api'] == None:
            api = {
                    # twitter
                    'twitter_key': '',
                    'twitter_key_secret': '',
                    'twitter_token': '',
                    'twitter_token_secret': '',
                    # reddit
                    'reddit_id': '',
                    'reddit_secret': '',
                    'reddit_agent': '',
                    'reddit_name': '',
                    'reddit_passwrd': ''
                }
            # Convert the dictionary into a JSON string
            api_json = json.dumps(api)
            db.execute("UPDATE users SET api = ? WHERE id = ?", api_json, userid)
            apiencrypted = db.execute("SELECT api FROM users WHERE id= ?", userid)
        # TODO: decrypte json with fermet
        apidecrypted =  apiencrypted
        apidecrypted = apidecrypted[0]['api']
        # Extract the data
        api_data = json.loads(apidecrypted)
        # api_data = apidecrypted
        twitter_key = api_data['twitter_key']
        twitter_key_secret = api_data['twitter_key_secret']
        twitter_token = api_data['twitter_token']
        twitter_token_secret = api_data['twitter_token_secret']
        reddit_id = api_data['reddit_id']
        reddit_secret = api_data['reddit_secret']
        reddit_agent = api_data['reddit_agent']
        reddit_username = api_data['reddit_name']
        reddit_password = api_data['reddit_passwrd']
        return render_template("api.html", reddit_id=reddit_id, reddit_secret=reddit_secret, reddit_agent=reddit_agent, reddit_username=reddit_username, reddit_password=reddit_password ,twitter_key=twitter_key, twitter_key_secret=twitter_key_secret, twitter_token=twitter_token, twitter_token_secret=twitter_token_secret)
    
    # api update/post info
    elif request.method == "POST":
        # Get the current API data from the database
        apiencrypted = db.execute("SELECT api FROM users WHERE id= ?", userid)
        apidecrypted = apiencrypted
        apidecrypted = apidecrypted[0]['api']
        api_data = json.loads(apidecrypted)

        # Update the API data with the new values from the form
        if request.form.get("twitter-key") and request.form.get("twitter-key") != api_data['twitter_key']:
            api_data['twitter_key'] = request.form.get("twitter-key")
        if request.form.get("twitter-key-secret") and request.form.get("twitter-key-secret") != api_data['twitter_key_secret']:
            api_data['twitter_key_secret'] = request.form.get("twitter-key-secret")
        if request.form.get("twitter-token") and request.form.get("twitter-token") != api_data['twitter_token']:
            api_data['twitter_token'] = request.form.get("twitter-token")
        if request.form.get("twitter-token-secret") and request.form.get("twitter-token-secret") != api_data['twitter_token_secret']:
            api_data['twitter_token_secret'] = request.form.get("twitter-token-secret")
        if request.form.get("reddit-id") and request.form.get("reddit-id") != api_data['reddit_id']:
            api_data['reddit_id'] = request.form.get("reddit-id")
        if request.form.get("reddit-secret") and request.form.get("reddit-secret") != api_data['reddit_secret']:
            api_data['reddit_secret'] = request.form.get("reddit-secret")
        if request.form.get("reddit-agent") and request.form.get("reddit-agent") != api_data['reddit_agent']:
            api_data['reddit_agent'] = request.form.get("reddit-agent")
        if request.form.get("reddit-username") and request.form.get("reddit-username") != api_data['reddit_name']:
            api_data['reddit_name'] = request.form.get("reddit-username")
        if request.form.get("reddit-password") and request.form.get("reddit-password") != api_data['reddit_passwrd']:
            api_data['reddit_passwrd'] = request.form.get("reddit-password")

        # Convert the updated API data back to a JSON string
        api_json = json.dumps(api_data)
        print(api_data)
        # Update the database with the new API data
        db.execute("UPDATE users SET api = ? WHERE id = ?", api_json, userid)

        return redirect("/api")
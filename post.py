import tweepy
import praw
import json
from cs50 import SQL
db = SQL("sqlite:///vigie.db")


# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
def tweet_create(msg, userid):
    apiencrypted = db.execute("SELECT api FROM users WHERE id= ?", userid)
    apidecrypted = apiencrypted
    apidecrypted = apidecrypted[0]['api']
    api_data = json.loads(apidecrypted)
    #twitter configs
    twitter_c_key = api_data['twitter_key']
    twitter_c_key_secret = api_data['twitter_key_secret']
    twitter_a_token = api_data['twitter_token']
    twitter_a_token_secret = api_data['twitter_token_secret']

    twitter = tweepy.Client(
        consumer_key=twitter_c_key,
        consumer_secret=twitter_c_key_secret,
        access_token=twitter_a_token,
        access_token_secret=twitter_a_token_secret
    )
    response = twitter.create_tweet(
        text=f"{msg}"
    )
    resplist = {"id":response.data['id'], "text":response.data['text'], "link": f"https://twitter.com/user/status/{response.data['id']}"}
    return resplist

'''
def tweet_poll(msg, poll_option_list, poll_duration):
    
    response = twitter.create_tweet(
        text=f"{msg}",
        poll_options=poll_option_list,
        poll_duration_minutes=poll_duration
    )
    return response.data['id'], response.data['text'], response.data['poll_options']
'''

# https://praw.readthedocs.io/en/stable/code_overview/other/submissionmoderation.html
def reddit_create(msg, title_reddit, userid):
    apiencrypted = db.execute("SELECT api FROM users WHERE id= ?", userid)
    apidecrypted = apiencrypted
    apidecrypted = apidecrypted[0]['api']
    api_data = json.loads(apidecrypted)
    #reddit configs
    reddit_id = api_data['reddit_id']
    reddit_secret = api_data['reddit_secret']
    reddit_agent = api_data['reddit_agent']
    reddit_name = api_data['reddit_name']
    reddit_passwrd = api_data['reddit_passwrd']
    
    reddit = praw.Reddit(
        client_id = reddit_id,
        client_secret = reddit_secret,
        user_agent = reddit_agent,
        username = reddit_name,
        password = reddit_passwrd)

    # get subreddit for publishing
    sub = "Tablerase"
    subreddit = reddit.subreddit(sub)
    # submit content
    submission = subreddit.submit(title=title_reddit, selftext=msg)

    resplist = {"id":submission.id, "link": f"https://reddit.com{submission.permalink}"}
    return resplist
import tweepy
import configparser
import praw

#read configs
config  = configparser.ConfigParser()
config.read('config.ini')

#twitter configs
bearer = config['twitter']['bearer']
twitter_c_key = config['twitter']['api_key']
twitter_c_key_secret = config['twitter']['api_key_secret']
twitter_a_token = config['twitter']['access_token']
twitter_a_token_secret = config['twitter']['access_token_secret']
#reddit configs
reddit_id = config['reddit']['client_id']
reddit_secret = config['reddit']['client_secret']
reddit_agent = config['reddit']['user_agent']
reddit_name = config['reddit']['username']
reddit_passwrd = config['reddit']['password']

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
def tweet_create(msg):
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
def reddit_create(msg, title_reddit):
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
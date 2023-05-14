import tweepy
import configparser

#read configs
config  = configparser.ConfigParser()
config.read('config.ini')

bearer = config['twitter']['bearer']
twitter_c_key = config['twitter']['api_key']
twitter_c_key_secret = config['twitter']['api_key_secret']
twitter_a_token = config['twitter']['access_token']
twitter_a_token_secret = config['twitter']['access_token_secret']
twitter = tweepy.Client(
        consumer_key=twitter_c_key,
        consumer_secret=twitter_c_key_secret,
        access_token=twitter_a_token,
        access_token_secret=twitter_a_token_secret
    )

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
def tweet_create(msg):
    
    response = twitter.create_tweet(
        text=f"{msg}"
    )
    resplist = {"id":response.data['id'], "text":response.data['text']}
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
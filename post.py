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

def tweet_create(msg):
    client = tweepy.Client(
        consumer_key=twitter_c_key,
        consumer_secret=twitter_c_key_secret,
        access_token=twitter_a_token,
        access_token_secret=twitter_a_token_secret
    )
    response = client.create_tweet(
        text=f"{msg}"

    )
    return response.data['id'], response.data['text']


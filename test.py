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


client = tweepy.Client(
        consumer_key=twitter_c_key,
        consumer_secret=twitter_c_key_secret,
        access_token=twitter_a_token,
        access_token_secret=twitter_a_token_secret
    )

response = client.create_tweet(
    text="This Tweet was Tweeted using Tweepy and Twitter API v2!"
)
print(f"https://twitter.com/user/status/{response.data['id']}")
resplist = { "id":response.data['id'], "text":response.data['text']}
print(response.data['id'])
print(response.data['text'])
print(resplist)

import configparser
import praw

#read configs
config  = configparser.ConfigParser()
config.read('config.ini')

client_id = config['reddit']['client_id']
client_secret = config['reddit']['client_secret']

reddit = praw.Reddit(
    client_id="Q3dfveBJYo_4FTwIdlKKmQ",
    client_secret="jUAAzmmqe9uVxOBqlJTUoZRxsAvAow",
    user_agent="_Tablerase",
)

# get subreddit for publishing
subreddit = reddit.subreddit("Tablerase")
print(subreddit.display_name)

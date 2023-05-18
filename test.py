import configparser
import praw

#read configs
config  = configparser.ConfigParser()
config.read('config.ini')

reddit_id = config['reddit']['client_id']
reddit_secret = config['reddit']['client_secret']
reddit_agent = config['reddit']['user_agent']
reddit_name = config['reddit']['username']
reddit_passwrd = config['reddit']['password']

print(reddit_id, reddit_secret, reddit_agent, reddit_name, reddit_passwrd)

reddit = praw.Reddit(
    client_id = reddit_id,
    client_secret = reddit_secret,
    user_agent = reddit_agent,
    username = reddit_name,
    password = reddit_passwrd)


# get subreddit for publishing
sub = "Tablerase"
subreddit = reddit.subreddit(sub)
submission = subreddit.submit(title="Test Submission", selftext="This is a test")

print(subreddit.display_name)
print(f"https://reddit.com{submission.permalink}")
print(submission.id)

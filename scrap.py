# api and scrape tools
import snscrape.modules.twitter as sntwitter
# test data scraped
import pandas as pd

def twitter_hashtag(tagname, limit):
    """twitter hashtag function"""
    # initiate values
    query = f"(#{tagname})"
    tweets = []
    
    # get tweets with limit
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
        # print(vars(tweet))
        # break
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.username, tweet.content])
    return tweets



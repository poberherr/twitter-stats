import tweepy
from app.twitter_fetch.twitter_api import api


def fetch_user_by_name(name):
    user_data = api.get_user(name)
    return user_data

def fetch_followers(id):
    '''
        Might overflow when follower count goes insane.
        The most popular version yo find out there is to slow,
        so I go with the simple approach for now
    '''
    follower_ids = api.followers_ids(id)
    return follower_ids

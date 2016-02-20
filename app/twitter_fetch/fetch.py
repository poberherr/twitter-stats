import tweepy
from app.twitter_fetch.twitter_api import api


def fetch_user_by_name(name):
    user_data = api.get_user(name)
    return user_data

def fetch_followers(id):
    ids = []
    for page in tweepy.Cursor(api.followers_ids, id=id).pages():
        pageid = pageid + 1
        ids.extend(page)

    return ids

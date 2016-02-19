from tweepy import OAuthHandler
import tweepy
import time

def fetch_user_by_name(name):
    import config
    auth = OAuthHandler(config.twitter['ckey'], config.twitter['csecret'])
    auth.set_access_token(config.twitter['atoken'], config.twitter['asecret'])

    api = tweepy.API(auth)
    user_data = api.get_user(name)
    return user_data

def get_followers(id):
    import config
    auth = OAuthHandler(config.twitter['ckey'], config.twitter['csecret'])
    auth.set_access_token(config.twitter['atoken'], config.twitter['asecret'])

    api = tweepy.API(auth)

    ids = []
    pageid = 0
    for page in tweepy.Cursor(api.followers_ids, id=id).pages():
        print(pageid)
        pageid = pageid + 1
        ids.extend(page)
        time.sleep(60)

    return ids

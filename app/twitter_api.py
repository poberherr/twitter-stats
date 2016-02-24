import config
import tweepy
from tweepy import OAuthHandler

def make_api():
    auth = OAuthHandler(config.twitter['ckey'], config.twitter['csecret'])
    auth.set_access_token(config.twitter['atoken'], config.twitter['asecret'])
    return tweepy.API(auth, wait_on_rate_limit=True)

twitter_api = make_api()

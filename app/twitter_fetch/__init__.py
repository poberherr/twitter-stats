from tweepy import OAuthHandler
import tweepy


def fetch_user_by_name(name):
    import config
    auth = OAuthHandler(config.twitter['ckey'], config.twitter['csecret'])
    auth.set_access_token(config.twitter['atoken'], config.twitter['asecret'])

    api = tweepy.API(auth)
    user_data = api.get_user(name)
    return user_data

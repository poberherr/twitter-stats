from app.twitter_api import twitter_api
from app.users.models import Users
from app.tweets.models import Tweets


def fetch_and_create_tweets(user):
    print('Fetching tweets for twitter_id: ', user.twitter_id)
    tweets_data = twitter_api.user_timeline(id=user.twitter_id, count=100)
    for tweet_data in tweets_data:
        tweet_exists = Tweets.query.filter_by(tweet_id=tweet_data.id).first()
        if not tweet_exists:
            print('Adding tweets for twitter_id: ', user.twitter_id)
            tweet = Tweets(tweet_data, user.id)
            tweet.add(tweet)
        if tweet_exists:
            print('Tweet ', tweet_exists.tweet_id, \
                'is already in the DB for user twitter_id:', user.twitter_id)
    tweets = Tweets.query.filter_by(user_id=user.id).\
        order_by(Tweets.created_at.desc()).limit(100)
    return tweets

from app.twitter_api import twitter_api
from app.users.models import Users
from app.tweets.models import Tweets


def fetch_and_create_tweets_by_id(twitter_id):
    print('Fetching tweets for twitter_id: ', twitter_id)
    tweets_data = twitter_api.user_timeline(id=twitter_id, count=100)
    user = Users.query.filter_by(twitter_id=twitter_id).first()
    for tweet_data in tweets_data:
        tweet_exists = Tweets.query.filter_by(tweet_id=tweet_data.id).first()
        if not tweet_exists:
            print('Adding tweets for twitter_id: ', twitter_id)
            tweet = Tweets(tweet_data, user.id)
            tweet.add(tweet)
        if tweet_exists:
            print('Tweet ', tweet_exists.tweet_id, 'is already in the DB for user twitter_id:', twitter_id)

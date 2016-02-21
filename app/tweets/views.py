from flask import Blueprint, request, jsonify, make_response
from app.tweets.models import Tweets, TweetsSchema, db
from app.users.models import Users
from app.twitter_fetch.fetch import fetch_tweets_by_screen_name
from flask_restful import Api, Resource

tweets = Blueprint('tweets', __name__)
api = Api(tweets)


class FetchTweetsByName(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            tweets = fetch_tweets_by_screen_name(screen_name)
            for tweet_data in tweets:
                tweet = Tweets(tweet_data, user.id)
                tweet.add(tweet)
        return

api.add_resource(FetchTweetsByName, '/<screen_name>')      # Retriving fetched users

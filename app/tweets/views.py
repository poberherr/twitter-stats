from flask import Blueprint, request, jsonify, make_response
from app.tweets.models import Tweets, TweetsSchema, db
from app.users.models import Users
from app.twitter_fetch.fetch_network import fetch_and_create_tweets_by_id
from flask_restful import Api, Resource

tweets = Blueprint('tweets', __name__)
api = Api(tweets)

# TODO: For consistency sake : Also add getting tweets by id
class FetchTweetsByName(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            tweets = fetch_and_create_tweets_by_id(user.twitter_id)
        # TODO: Manually create tweet schema here again :S
        return

api.add_resource(FetchTweetsByName, '/<screen_name>')      # Retriving fetched tweets

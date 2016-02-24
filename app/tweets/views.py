from flask import Blueprint, request, jsonify, make_response
from app.tweets.models import Tweets, TweetsSchema, db
from app.users.models import Users
from app.tweets.fetch_tweets import fetch_and_create_tweets
from flask_restful import Api, Resource

tweets = Blueprint('tweets', __name__)
api = Api(tweets)

class FetchTweetsById(Resource):

    def get(self, id):
        user = Users.query.get_or_404(id)
        if user:
            tweets = fetch_and_create_tweets(user)
            # TODO: create tweet output schema
            return
        return 'User doesn\'t exist', 404

class FetchTweetsByName(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            tweets = fetch_and_create_tweets(user)
        # TODO: Manually create tweet schema here again :S
        return

api.add_resource(FetchTweetsById, '/<int:id>')
api.add_resource(FetchTweetsByName, '/<screen_name>')      # Retriving fetched tweets

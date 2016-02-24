import numpy
import json
from collections import Counter

from flask import Blueprint
from flask.ext.cors import CORS

from app.users.models import Users
from app.users.fetch_users import fetch_twitter_screen_name_to_twitter_id,\
    fetch_and_create_user
from app.users.fetch_users import create_users_in_bulk
from app.tweets.models import Tweets
from app.tweets.fetch_tweets import fetch_and_create_tweets
from app.followers.fetch_followers import fetch_followers_from_db,\
    fetch_and_create_followers
from app.statistics.statistics import get_statistics
from app.statistics.schema import create_statistics_schema
from flask_restful import Api, Resource

from sqlalchemy import desc, asc, func


statistics = Blueprint('statistics', __name__)
CORS(statistics)
api = Api(statistics)

#
# def get_complete_user_network(twitter_id):
#     print('Fetching user with twitter_id: ', twitter_id)
#     user = fetch_and_create_user_by_id(twitter_id)
#     fetch_and_create_tweets(twitter_id)
#     create_followers_if_not_exist(user)
#     for user in tweepy.Cursor(api.followers, id=twitter_id).items():
#         current_follower = create_user_if_not_exists(user)


class TweetStatistics(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if not user:
            twitter_id = fetch_twitter_screen_name_to_twitter_id(screen_name)
            user = fetch_and_create_user(twitter_id)

        # could be skipped for better performance
        if user.is_follower_fetched:
            follower_ids = fetch_followers_from_db(user)
        else:
            follower_ids = fetch_and_create_followers(user)

        # could be skipped for better performance
        users = create_users_in_bulk(user);
        '''
            We have all the follower_ids and need to make a bulk
            lookup to fetch roots users followers to calculate
            max_reach count
        '''
        # They always need to be fresh
        tweets = fetch_and_create_tweets(user)
        statistics = get_statistics(user, tweets) # TODO: followers
        result = create_statistics_schema(user, statistics)
        return result, 201

api.add_resource(TweetStatistics, '/<screen_name>')

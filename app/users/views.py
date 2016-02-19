from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema, db
from app.twitter_fetch import fetch_user_by_name
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError

from marshmallow import ValidationError

from tweepy import OAuthHandler
import tweepy


users = Blueprint('users', __name__)

# Helpful links
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = UsersSchema()
api = Api(users)

# Users
class UsersList(Resource):
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""
    def get(self):
        users_query = Users.query.all()
        results = schema.dump(users_query, many=True).data
        return results



class UserFetch(Resource):

    def get(self, id):
        users_query = Users.query.get_or_404(id)
        result = schema.dump(users_query).data
        return result


class UserByName(Resource):

    def get(self, name):
<<<<<<< Updated upstream
=======

        # ckey="JJwDjqFg4IW372BcwiVkkhQ1Z"
        # csecret="s0QMMvm6dpeF7uRqoetTkJjVrd56Co7cLWJ4p1SNTJKtYnzLdP"
        # atoken="48399689-yd0KnEE24Ye1bf21iu2KlQmwvMCkPrU0p3eMWKNbR"
        # asecret="bBE12wEEP9Kyp7kVUZUQjVFhnHbldikqQM58b5cAQ0yw5"
        #
        # auth = OAuthHandler(ckey, csecret)
        # auth.set_access_token(atoken, asecret)
        #
        # api = tweepy.API(auth)
        # Get information about the user

        # user_data = api.get_user(name)
>>>>>>> Stashed changes
        user_data = fetch_user_by_name(name)

        user = Users( user_data.id,
            user_data.name, user_data.screen_name, user_data.location,
            user_data.description, user_data.url, user_data.followers_count,
            user_data.friends_count, user_data.created_at, user_data.favourites_count,
            user_data.time_zone, user_data.statuses_count)
        try:
            user.add(user)
        except IntegrityError:
            return 'User was already fetched', 409

        query = Users.query.get(user.id)
        results = schema.dump(query).data
        return results, 201


api.add_resource(UsersList, '')
api.add_resource(UserFetch, '/<int:id>')      # Retriving fetched users
api.add_resource(UserByName, '/<name>')     # Fetch a user by name from twitter

from flask import Blueprint

from app.followers.models import Followers
from app.followers.fetch_followers import fetch_and_create_followers,\
    fetch_followers_from_db
from app.followers.schema import create_follower_schema
from app.users.models import Users
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError


followers = Blueprint('followers', __name__)
api = Api(followers)

'''
    Normally we would have a data model of one twitter id and a list of
    the followers. I wanted a 'proper' many to many relationship.
    Because of that the REST logic gets a bit weird and also the schema of
    followers in app.followers.models doesn't fit.
    For now I would just like to continue with it since the interesting parts
    are yet to come :)
'''

class FollowFetchById(Resource):

    def get(self, id):
        user = Users.query.get_or_404(id)
        if user:
            if user.is_follower_fetched:
                follower_ids = fetch_followers_from_db(user)
                return create_follower_schema(user, follower_ids), 200
            else:
                follower_ids = fetch_and_create_followers(user)
                return create_follower_schema(user, follower_ids), 201
        return '{}', 404

# TODO: fix it !
# class FollowFetchByName(Resource):
#
#     def get(self, screen_name):
#         user = Users.query.filter_by(screen_name=screen_name).first()
#         if user:
#             return create_follower_schema(user), 200
#         return '{}', 404

api.add_resource(FollowFetchById, '/<int:id>')      # Retriving fetched followers
# api.add_resource(FollowFetchByName, '/<screen_name>')      # Retriving fetched followers

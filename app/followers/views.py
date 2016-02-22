from flask import Blueprint

from app.followers.models import Followers, FollowerSchema
from app.users.models import Users
from app.twitter_fetch.fetch_network import create_followers_if_not_exist
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError


followers = Blueprint('followers', __name__)
schema = FollowerSchema()
api = Api(followers)

'''
    Normally we would have a data model of one twitter id and a list of
    the followers. I wanted a 'proper' many to many relationship.
    Because of that the REST logic gets a bit weird and also the schema of
    followers in app.followers.models doesn't fit.
    For now I would just like to continue with it since the interesting parts
    are yet to come :)
'''

def create_follower_schema(user):
    follower_ids = create_followers_if_not_exist(user)
    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'followers': [follower_ids]
        }}}
    return result

class FollowFetchById(Resource):

    def get(self, id):
        user = Users.query.get_or_404(id)
        if user:
            return create_follower_schema(user), 200
        return '{}', 404

class FollowFetchByName(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            return create_follower_schema(user), 200
        return '{}', 404

api.add_resource(FollowFetchById, '/<int:id>')      # Retriving fetched followers
api.add_resource(FollowFetchByName, '/<screen_name>')      # Retriving fetched followers

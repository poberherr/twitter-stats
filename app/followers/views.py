from flask import Blueprint

from app.followers.models import Followers, FollowerSchema
from app.users.models import Users
from app.twitter_fetch.fetch import get_followers
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError


followers = Blueprint('followers', __name__)
schema = FollowerSchema()
api = Api(followers)

class FollowFetch(Resource):

    def get(self, id):
        user = Users.query.get_or_404(id)
        if user:
            follower_ids = get_followers(user)
            result = {'data': {'attributes': {
                    'id': user.id,
                    'twitter_id': user.twitter_id,
                    'followers': [follower_ids]
                }}}
            return result, 200
        return '{}', 404

    '''
        Normally we would have a data model of one twitter id and a list of
        the followers. I wanted a 'proper' many to many relationship.
        Because of that the REST logic gets a bit weird and also the schema of
        followers in app.followers.models doesn't fit.
        For now I would just like to continue with it since the interesting parts
        are yet to come :)
    '''

api.add_resource(FollowFetch, '/<int:id>')      # Retriving fetched followers

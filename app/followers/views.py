from flask import Blueprint

from app.followers.models import Followers, FollowerSchema
from app.users.models import Users
from app.twitter_fetch.fetch import fetch_followers
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError


followers = Blueprint('followers', __name__)
schema = FollowerSchema()
api = Api(followers)

class FollowFetch(Resource):

    def get(self, id):
        followers = Followers.query.filter_by(user_id=id).all()
        if followers:
            follower_ids = []
            for follower in followers:
                follower_ids.append(follower.twitter_follower_id)
            result = {'data': {'attributes': {
                    'id': followers[0].user_id,
                    'twitter_id': followers[0].twitter_id,
                    'followers': [follower_ids]
                }}}
            return result, 200
        else:
            # Get from internal user_id to twitter_id
            user = Users.query.get_or_404(id)
            if user:
                all_followers = fetch_followers(user.twitter_id)
                for follower_id in all_followers:
                    follower = Followers(id, user.twitter_id, follower_id)
                    follower.add(follower)

                result = {'data': {'attributes': {
                        'id': user.id,
                        'twitter_id': user.twitter_id,
                        'followers': [all_followers]
                    }}}
                return result, 200
            return response

    '''
        Normally we would have a data model of one twitter id and a list of
        the followers. I wanted a 'proper' many to many relationship.
        Because of that the REST logic gets a bit weird and also the schema of
        followers in app.followers.models doesn't fit.
        For now I would just like to continue with it since the interesting parts
        are yet to come :)
    '''

api.add_resource(FollowFetch, '/<int:id>')      # Retriving fetched followers

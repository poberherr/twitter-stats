from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema, db
from app.twitter_fetch.fetch_network import twitter_screen_name_to_id, fetch_and_create_user_by_id
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError

from marshmallow import ValidationError


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
        user = Users.query.get_or_404(id)
        result = schema.dump(user).data
        return result

    def delete(self, id):
        user = Users.query.get_or_404(id)
        try:
            delete = user.delete(user)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UserFetchByName(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            result = schema.dump(user).data
            return result, 200
        else:
            twitter_id = twitter_screen_name_to_id(screen_name)
            user = fetch_and_create_user_by_id(twitter_id)
            results = schema.dump(user).data
            return results, 201

        # TODO: Call here the fetching of all the friends from the "main" user
        # so that the request can return and the fetching takes place in the
        # background

api.add_resource(UsersList, '')
api.add_resource(UserFetch, '/<int:id>')      # Retriving fetched users
api.add_resource(UserFetchByName, '/<screen_name>')     # Fetch a user by name from twitter

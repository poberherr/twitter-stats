from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema, db
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError
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
        users_query = Users.query.get_or_404(id)
        result = schema.dump(users_query).data
        return result


class UserByName(Resource):

    def get(self, name):
        # import pdb; pdb.set_trace()
        users_query = Users.query.filter(Users.name == name).first()
        result = schema.dump(users_query).data
        return result


api.add_resource(UsersList, '')
api.add_resource(UserGet, '/<int:id>')      # Retriving fetched users
api.add_resource(UserByName, '/<name>')     # Fetch a user by name from twitter

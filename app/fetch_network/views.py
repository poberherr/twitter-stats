from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users
from app.twitter_fetch.fetch_network import get_complete_user_network, twitter_screen_name_to_id
from flask_restful import Api, Resource

fetch_network = Blueprint('fetch_network', __name__)
api = Api(fetch_network)


class FetchNetworkByName(Resource):

    def get(self, screen_name):
        twitter_id = twitter_screen_name_to_id(screen_name)
        get_complete_user_network(twitter_id)
        return


class FetchNetworkById(Resource):

    def get(self, id):
        user = Users.quer.filter_by(id=id).first()
        get_complete_user_network(user.twitter_id)
        return

api.add_resource(FetchNetworkById, '/<int:id>')      # Retriving fetched users
api.add_resource(FetchNetworkByName, '/<screen_name>')      # Retriving fetched users

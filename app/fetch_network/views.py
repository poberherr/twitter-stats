from flask import Blueprint, request, jsonify, make_response
from app.twitter_fetch.fetch import fetch_user_network, twitter_screen_name_to_id
from flask_restful import Api, Resource

fetch_network = Blueprint('fetch_network', __name__)
api = Api(fetch_network)


class FetchNetworkByName(Resource):

    def get(self, screen_name):
        twitter_id = twitter_screen_name_to_id(screen_name)
        fetch_user_network(twitter_id, 0, 2)
        return


class FetchNetworkById(Resource):

    def get(self, id):
        fetch_user_network(id, 0, 2)
        return

api.add_resource(FetchNetworkById, '/<int:id>')      # Retriving fetched users
api.add_resource(FetchNetworkByName, '/<screen_name>')      # Retriving fetched users

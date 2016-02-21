import tweepy
from app.users.models import Users
from app.followers.models import Followers
from app.twitter_fetch.twitter_api import api

from sqlalchemy.exc import IntegrityError

def twitter_screen_name_to_id(screen_name):
    user_data = api.get_user(screen_name)
    return user_data.id

def fetch_and_create_user_by_id(twitter_id):
    user = Users.query.filter_by(twitter_id=twitter_id).first()
    if user:
        return user
    else:
        user_data = api.get_user(twitter_id)
        user = Users(user_data)
        user.add(user)
        user = Users.query.get(user.id)
    return user

def retrieve_followers_from_db(user):
    followers = Followers.query.filter_by(user_id=user.id).all()
    if followers:
        follower_ids = []
        for follower in followers:
            follower_ids.append(follower.twitter_follower_id)
        return follower_ids
    return

def get_followers(user):
    if user.is_follower_fetched:
        follower_ids = retrieve_followers_from_db(user)
    else:
        follower_ids = api.followers_ids(user.twitter_id)
        for follower_id in follower_ids:
            follower = Followers(user.id, user.twitter_id, follower_id)
            follower.add(follower)
        user.is_follower_fetched = True
        user.update()
    return follower_ids

def fetch_user_network(twitter_id, depth, max_depth):
    if depth == max_depth:
        return
    user = fetch_and_create_user_by_id(twitter_id)
    if depth == 0:
        all_user_followers = get_followers(user)
        for follower in all_user_followers:
            fetch_user_network(follower, depth + 1, max_depth)
    return

def fetch_tweets_by_screen_name(screen_name):
    #  TODO: retrieve set of tweet id's and compare with db content_type
    # after finding the 'new' one's: insert
    tweet_data = api.user_timeline(screen_name=screen_name, count=100)
    return tweet_data

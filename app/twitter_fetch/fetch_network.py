import tweepy
from app.users.models import Users
from app.followers.models import Followers
from app.tweets.models import Tweets
from app.twitter_fetch.twitter_api import api

def twitter_screen_name_to_id(screen_name):
    user = Users.query.filter_by(screen_name=screen_name).first()
    if user:
        return user.twitter_id
    else:
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

def fetch_and_create_tweets_by_id(twitter_id):
    print('Fetching tweets for twitter_id: ', twitter_id)
    tweets_data = api.user_timeline(id=twitter_id, count=100)
    user = Users.query.filter_by(twitter_id=twitter_id).first()
    print('Creating tweets for twitter_id: ', twitter_id)
    for tweet_data in tweets_data:
        tweet_exists = Tweets.query.filter_by(tweet_id=tweet_data.id).first()
        if not tweet_exists:
            tweet = Tweets(tweet_data, user.id)
            tweet.add(tweet)
    return

def create_user_if_not_exists(user_data):
    user = Users.query.filter_by(twitter_id=user_data.id).first()
    if user:
        print('User ', user.screen_name, ' was already in DB')
        return user
    else:
        user = Users(user_data)
        user.add(user)
        user = Users.query.get(user.id)
        print('Creating user in DB: ', user.screen_name)
    return user

def retrieve_followers_from_db(user):
    followers = Followers.query.filter_by(user_id=user.id).all()
    if followers:
        follower_ids = []
        for follower in followers:
            follower_ids.append(follower.twitter_follower_id)
        return follower_ids
    return

def create_followers_if_not_exist(user):
    # For now we assume the followers don't change
    if user.is_follower_fetched:
        print('User was already in DB :', user.screen_name)
        follower_ids = retrieve_followers_from_db(user)
    else:
        try:
            print('Fetching followers for: ', user.screen_name)
            follower_ids = api.followers_ids(user.twitter_id)
            print('Inserting followers for: ', user.screen_name)
            for follower_id in follower_ids:
                follower = Followers(user.id, user.twitter_id, follower_id)
                follower.add(follower)
            user.is_follower_fetched = True
            user.update()
            return follower_ids
        except tweepy.TweepError as e:
            # set flag in user that followers are private
            print(e)
            return
    return follower_ids

def get_complete_user_network(twitter_id):
    # get user
    print('Fetching user with twitter_id: ', twitter_id)
    user = fetch_and_create_user_by_id(twitter_id)

    # get tweets
    fetch_and_create_tweets_by_id(twitter_id)

    # get all follower id's
    create_followers_if_not_exist(user)

    # take all follower id's and create Users
    for user in tweepy.Cursor(api.followers, id=twitter_id).items():
        current_follower = create_user_if_not_exists(user)
        # for each follower_id get followers
        create_followers_if_not_exist(current_follower)

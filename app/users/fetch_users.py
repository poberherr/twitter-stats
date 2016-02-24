import tweepy
from app.twitter_api import twitter_api
from app.users.models import Users

def fetch_twitter_screen_name_to_twitter_id(screen_name):
    user = Users.query.filter_by(screen_name=screen_name).first()
    if user:
        return user.twitter_id
    else:
        try:
            print('Fetching twitter_id from screem_name: ', screen_name)
            user_data = twitter_api.get_user(screen_name)
        except tweepy.TweepError as e:
            # https://github.com/tweepy/tweepy/issues/209
            return
        return user_data.id

# Fetches just the user to be investigated
def fetch_and_create_user(twitter_id):
    user = Users.query.filter_by(twitter_id=twitter_id).first()
    if user:
        return user
    else:
        print('Fetching user from twitter with twitter_id:', twitter_id)
        user_data = twitter_api.get_user(twitter_id)
        user = Users(user_data)
        user.add(user)
        user = Users.query.get(user.id)
    return user

def create_users_in_bulk(existing_user):
    user_list = []
    print('Starting bulk loading of users -->')
    for user in tweepy.Cursor(twitter_api.followers, id=existing_user.twitter_id).pages():
        print('123')
        user_db = Users.query.filter_by(twitter_id=user.id).first()
        if user_db:
            print('User exists - taking user from db')
            user_list.append(user_db)
        else:
            print('Creating user in bulk operation: ', user.screen_name)
            new_user = Users(user)
            user.add(new_user)
            user_list.append(user)
    print('Finished bulk loading of users <--')
    return user_list

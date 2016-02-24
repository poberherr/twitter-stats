import tweepy
from app.twitter_api import twitter_api
from app.users.models import Users



# Stays
def fetch_twitter_screen_name_to_twitter_id(screen_name):
    user = Users.query.filter_by(screen_name=screen_name).first()
    if user:
        return user.twitter_id
    else:
        try:
            user_data = twitter_api.get_user(screen_name)
        except tweepy.TweepError as e:
            # https://github.com/tweepy/tweepy/issues/209
            return
        return user_data.id

# Fetches just the user to be investigated
def fetch_and_create_root_user_by_id(twitter_id):
    user = Users.query.filter_by(twitter_id=twitter_id).first()
    if user:
        return user
    else:
        user_data = twitter_api.get_user(twitter_id)
        user = Users(user_data)
        user.add(user)
        user = Users.query.get(user.id)
    return user

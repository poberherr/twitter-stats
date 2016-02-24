from app.followers.models import Followers

def fetch_and_create_followers(user):
    # For now we assume the followers don't change
    if user.is_follower_fetched:
        print('User was already in DB :', user.screen_name)
        follower_ids = retrieve_followers_from_db(user)
    else:
        try:
            print('Fetching followers for: ', user.screen_name)
            # TODO: This call fetches 'just' 5000 followers
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
            return None, e
    return follower_ids

def fetch_followers_from_db(user):
    followers = Followers.query.filter_by(user_id=user.id).all()
    if followers:
        follower_ids = []
        for follower in followers:
            follower_ids.append(follower.twitter_follower_id)
        return follower_ids

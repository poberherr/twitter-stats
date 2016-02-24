def create_follower_schema(user, follower_ids):
    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'followers': [follower_ids]
        }}}
    return result

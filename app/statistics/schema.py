from app.users.models import UsersSchema
user_schema = UsersSchema()

def create_statistics_schema(user, stat):
    if bool(stat):
        keys = ['source', 'count']
        user_devices = [dict(zip(keys,value)) for value in stat['user_sources']]
        words_used = [dict(zip(keys,value)) for value in stat['most_words_used']]
    else:
        keys = []; user_devices = []; words_used = []
        stat['tweet_count'] = 0
        stat['perc_of_own_tweets'] = 0
        stat['daily_stats'] = 0
    user_info = user_schema.dump(user).data

    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'tweets_analysed': stat['tweet_count'],
            'user_devices': user_devices,
            'perc_of_own_tweets_vs_retweeted': stat['perc_of_own_tweets'],
            'most_words_used': words_used,
            'stats_per_day': stat['daily_stats']
        }}, 'user': user_info}
    return result

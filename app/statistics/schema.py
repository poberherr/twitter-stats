from app.users.models import UsersSchema
user_schema = UsersSchema()

def create_statistics_schema(user, stat):
    if bool(stat):
        keys = ['source', 'count']
        user_devices = [dict(zip(keys,value)) for value in stat['user_sources']]
        words_used = [dict(zip(keys,value)) for value in stat['most_words_used']]
        top_reply_users = [dict(zip(keys,value)) for value in stat['top_reply_users']]
    else:
        keys = []; user_devices = []; words_used = []
        stat['tweet_count'] = 0
        stat['perc_of_own_tweets'] = 0
        stat['daily_stats'] = 0
    user_info = user_schema.dump(user).data

    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'user_got_retweeted_count': stat['user_got_retweeted_count'],
            'avg_own_tweets_vs_retweeted_count': round(stat['avg_own_tweets_vs_retweeted_count'], 2),
            'tweets_analysed': stat['tweet_count'],
            'user_devices': user_devices,
            'perc_of_own_tweets_vs_retweeted': round(stat['perc_of_own_tweets'], 2),
            'most_words_used': words_used,
            'average_stars': round(stat['avg_stars'], 2),
            'mean_stars': round(stat['mean_stars'], 2),
            'average_retweets': round(stat['avg_retweets'],2),
            'mean_retweets': round(stat['mean_retweets'], 2),
            'top_reply_users': top_reply_users,
            'stats_per_day': stat['daily_stats']
        }}, 'user': user_info}
    return result

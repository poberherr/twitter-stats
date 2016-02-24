def create_statistics_schema(user, stat):
    keys = ['source', 'count']
    user_devices = [dict(zip(keys,value)) for value in stat['user_sources']]
    words_used = [dict(zip(keys,value)) for value in stat['most_words_used']]
    prec_of_own_tweets = 1 - stat['retweet_counter'] / stat['tweet_count']
    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'tweets_analysed': stat['tweet_count'],
            'user_devices': user_devices,
            'prec_of_own_tweets_vs_retweeted': prec_of_own_tweets,
            'most_words_used': words_used,
            'stats_per_day': stat['daily_stats']
        }}}
    return result

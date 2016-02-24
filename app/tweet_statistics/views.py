import numpy
import json
from collections import Counter

from flask import Blueprint
from flask.ext.cors import CORS

from app.users.models import Users
from app.tweets.models import Tweets
from app.tweet_statistics.statistics import \
    get_most_frequent_words, get_average_stars
from flask_restful import Api, Resource

from sqlalchemy import desc, asc, func


tweet_statistics = Blueprint('tweet_statistics', __name__)
CORS(tweet_statistics)
api = Api(tweet_statistics)

def get_tweet_data_by_day(tweets):
    dates = []
    tweets_per_day = []
    fav_count_per_day = []
    retw_count_per_day = []
    for tweet in tweets:
        if tweet.created_at.date() not in dates:
            dates.append(tweet.created_at.date())

    [tweets_per_day.append(0) for date in dates]
    [fav_count_per_day.append(0) for date in dates]
    [retw_count_per_day.append(0) for date in dates]
    dates = dates[::-1]

    for tweet in tweets:
        dx = dates.index(tweet.created_at.date())
        tweets_per_day[dx] = tweets_per_day[dx] + 1
        fav_count_per_day[dx] = fav_count_per_day[dx] + tweet.favorite_count
        retw_count_per_day[dx] = retw_count_per_day[dx] + tweet.retweet_count

    dates = [date.strftime('%Y-%m-%d') for date in dates]

    dates.insert(0,'x')
    tweets_per_day.insert(0,'tweets_per_day')
    fav_count_per_day.insert(0,'likes_per_day')
    retw_count_per_day.insert(0,'popular_retweets_you_also_retweeted')

    res = []
    res.append(dates)
    res.append(tweets_per_day)
    res.append(fav_count_per_day)
    # often to big and blurrs info in chart
    # uncomment to test
    # res.append(retw_count_per_day)
    return res


def create_statistics_schema(user, tweets, stat):
    keys = ['source', 'count']
    user_devices = [dict(zip(keys,value)) for value in stat['user_sources']]
    words_used = [dict(zip(keys,value)) for value in stat['most_words_used']]
    prec_of_own_tweets = 1 - stat['retweet_counter'] / stat['tweet_count']
    daily_stats = get_tweet_data_by_day(tweets)
    result = {'data': {'attributes': {
            'id': user.id,
            'twitter_id': user.twitter_id,
            'tweets_analysed': stat['tweet_count'],
            'user_devices': user_devices,
            'prec_of_own_tweets_vs_retweeted': prec_of_own_tweets,
            'most_words_used': words_used,
            'stats_per_day': daily_stats
        }}}
    return result


class TweetStatistics(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            tweets = Tweets.query.filter_by(user_id=user.id).\
                order_by(Tweets.created_at.desc()).limit(100)

            stat = {}
            most_words_used = get_most_frequent_words(tweets)
            stat['most_words_used'] = most_words_used

            avg_stars = numpy.average([tweet.favorite_count for tweet in tweets])
            # print('Average of stars per tweet: ', avg_stars)
            mean_stars = numpy.mean([tweet.favorite_count for tweet in tweets])
            # print('Mean of stars per tweet: ', avg_stars)

            avg_retweets = numpy.average([tweet.is_retweet for tweet in tweets])
            # print('Average of retweets per tweet: ', avg_retweets)
            mean_retweets = numpy.mean([tweet.is_retweet for tweet in tweets])
            # print('Mean of retweets per tweet: ', avg_retweets)

            stat['tweet_count'] = 0
            stat['reply_counter'] = 0
            stat['retweet_counter'] = 0
            for tweet in tweets:
                stat['tweet_count'] = stat['tweet_count'] + 1
                if tweet.in_reply_to_user_id:
                    stat['reply_counter'] = stat['reply_counter'] + 1
                if tweet.is_retweet:
                    stat['retweet_counter'] = stat['retweet_counter'] + 1
            # print('Retweet counter: ', stat['retweet_counter'])
            # print('Average percent of replies: ', stat['reply_counter'])
            # print('Average precent of retweets per tweets:', stat['retweet_counter'])

            top_reply_users = Counter([tweet.in_reply_to_screen_name for tweet in tweets\
                if tweet.in_reply_to_screen_name]).most_common(5)
            print('Top users you replied to: ', top_reply_users)

            sources = [tweet.source for tweet in tweets if (tweet.source)]
            stat['user_sources'] = Counter(sources).most_common(10)

            return create_statistics_schema(user, tweets, stat)

        return 'No User'

api.add_resource(TweetStatistics, '/<screen_name>')

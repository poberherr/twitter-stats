import numpy
from collections import Counter

from flask import Blueprint
from app.users.models import Users
from app.tweets.models import Tweets
from app.tweet_statistics.statistics import \
    get_most_frequent_words, get_average_stars
from flask_restful import Api, Resource

from sqlalchemy import desc, asc


tweet_statistics = Blueprint('tweet_statistics', __name__)
api = Api(tweet_statistics)

class TweetStatistics(Resource):

    def get(self, screen_name):
        user = Users.query.filter_by(screen_name=screen_name).first()
        if user:
            tweets = Tweets.query.filter_by(user_id=user.id).\
                order_by(Tweets.created_at.desc()).limit(100)

            most_words_used = get_most_frequent_words(tweets)
            print('Most words used: ', most_words_used)


            avg_stars = numpy.average([tweet.favorite_count for tweet in tweets])
            print('Average of stars per tweet: ', avg_stars)
            mean_stars = numpy.mean([tweet.favorite_count for tweet in tweets])
            print('Mean of stars per tweet: ', avg_stars)

            avg_retweets = numpy.average([tweet.is_retweet for tweet in tweets])
            print('Average of retweets per tweet: ', avg_retweets)
            mean_retweets = numpy.mean([tweet.is_retweet for tweet in tweets])
            print('Mean of retweets per tweet: ', avg_retweets)

            reply_counter = 0
            retweet_counter = 0
            for tweet in tweets:
                if tweet.in_reply_to_user_id:
                    reply_counter = reply_counter + 1
                if tweet.is_retweet:
                    retweet_counter = retweet_counter + 1
            print('Average percent of replies: ', reply_counter)
            print('Average precent of retweets per tweets:', retweet_counter)

            top_reply_users = Counter([tweet.in_reply_to_screen_name for tweet in tweets\
                if tweet.in_reply_to_screen_name]).most_common(5)
            print('Top users you replied to: ', top_reply_users)

            return avg_stars

        return 'No User'

api.add_resource(TweetStatistics, '/<screen_name>')

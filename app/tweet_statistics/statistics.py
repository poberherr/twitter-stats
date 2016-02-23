import numpy
from collections import Counter

def get_most_frequent_words(tweets):
    all_tweet_text = ''
    for tweet in tweets:
        all_tweet_text = all_tweet_text + ' ' + tweet.text
    words = all_tweet_text.split(' ')
    common_words = frozenset((
    'if', 'but', 'and', 'the', 'when', 'use', 'to', 'for',
    'via', 'the', 'rt', '-', 'to', 'of', 'in', 'for', 'on', 'with',
    'at', 'by', 'no', 'yes', '!', 'more', 'still', 'how',
    'from', 'up', 'about', 'into', 'over', 'after', 'beneath',
    'under', 'above', 'me', 'your', 'has', 'can', 'have', '/',
    'the', 'are', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you',
    'this', 'but',
    'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would',
    'there', 'their', 'und', 'is', 'die', '', 'für', 'im', 'das', 'ist',
    'du', 'ich', 'nicht', 'die', 'es', 'und', 'sie', 'der', 'was',
    'wir', 'zu', 'ein', 'er', 'in', 'mir', 'mit', 'ja', 'wie', 'den',
    'auf', 'mich', 'dass', 'daß', 'so', 'hier', 'eine', 'wenn', 'hat',
    'all', 'sind', 'von', 'dich', 'war', 'haben', 'an', 'habe', 'da',
    'nein', 'bin', 'noch', 'dir', 'uns', 'sich', 'nur', 'einen',
    'kann', 'dem', 'bei'))
    lower_words = [word.lower() for word in words if (word.lower() not in common_words)]
    word_counts = Counter(lower_words).most_common(10)
    # for word in word_counts:
    #     print(word[0], word[1])
    return word_counts

def get_average_stars(tweets):
    # favorite_count
    avg_stars = numpy.mean([tweet.favorite_count for tweet in tweets])
    return avg_stars

def get_average_retweets(tweets):
    # retweet_count
    avg_retweets = numpy.mean([tweet.retweet_count for tweet in tweets])
    return avg_retweets

def get_percentage_of_responses_by_user(tweets):
    # is_reply_to_user_id
    response_perc = numpy.persentile([tweet.is_reply_to_user_id for tweet in tweets])
    return response_prec

def get_percentage_of_user_retweets(tweets):
    # is_retweet
    retweet_perc = numpy.persentile([tweet.is_retweet for tweet in tweets])
    return retweet_perc

def get_top_reply_users(tweets):
    # in_reply_to_screen_name
    top_reply_users = Counter([tweets.screen_name for tweet in tweets])
    return top_reply_users

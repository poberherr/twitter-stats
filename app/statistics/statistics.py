import numpy
import re
from collections import Counter

def get_most_frequent_words(tweets):
    all_tweet_text = ''
    for tweet in tweets:
        all_tweet_text = all_tweet_text + ' ' + tweet.text
    re.sub(r'[^\w]', '', all_tweet_text)
    words = all_tweet_text.split(' ')
    common_words = frozenset((
    'if', 'but', 'and', 'the', 'when', 'use', 'to', 'for', 'do', 'be',
    'via', 'the', 'rt', '-', 'to', 'of', 'in', 'for', 'on', 'with', 'don\'t',
    'at', 'by', 'no', 'yes', '!', 'more', 'still', 'how', 'just', 'like',
    'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'out',
    'under', 'above', 'me', 'your', 'has', 'can', 'have', '/',
    'the', 'are', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you',
    'this', 'but', 'some', 'what', 'get', 'man', '@',
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
    return word_counts

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
    # res.append(retw_count_per_day)
    return res


def get_statistics(user, tweets):
    stat = {}
    try:
        tweets[0]
    except IndexError:
        return stat


    stat['daily_stats'] = get_tweet_data_by_day(tweets)
    stat['most_words_used'] = get_most_frequent_words(tweets)

    stat['avg_stars'] = numpy.average([tweet.favorite_count for tweet in tweets])
    stat['mean_stars'] = numpy.mean([tweet.favorite_count for tweet in tweets])
    stat['avg_retweets'] = numpy.average([tweet.is_retweet for tweet in tweets])
    stat['mean_retweets'] = numpy.mean([tweet.is_retweet for tweet in tweets])
    stat['top_reply_users'] = Counter([tweet.in_reply_to_screen_name for tweet in tweets\
        if tweet.in_reply_to_screen_name]).most_common(5)

    stat['tweet_count'] = 0
    stat['reply_counter'] = 0
    stat['retweet_counter'] = 0
    stat['perc_of_own_tweets'] = 0



    for tweet in tweets:
        stat['tweet_count'] = stat['tweet_count'] + 1
        if tweet.in_reply_to_user_id:
            stat['reply_counter'] = stat['reply_counter'] + 1
        if tweet.is_retweet:
            stat['retweet_counter'] = stat['retweet_counter'] + 1

    sources = [tweet.source for tweet in tweets if (tweet.source)]
    stat['user_sources'] = Counter(sources).most_common(10)

    if stat['tweet_count'] != 0:
        placeholder = 1 - stat['retweet_counter'] / stat['tweet_count']
        stat['perc_of_own_tweets'] = placeholder
    # else:
    #     stat['perc_of_own_tweets'] = 0
    return stat

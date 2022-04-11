import re
import csv

import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler


def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', " ", tweet).split())


def get_tweet_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'b5HGk1yrP7pgtWCsqTgRcEog1'
        consumer_secret = 'gxkCznbQ6Vja5X94TTVklxb726AuUYvjcHGQZnatvv0T582b5p'
        access_token = '766580899693535232-tZmLUdg2Y8J9nbbJOiSVH4cDvB3hiZY'
        access_token_secret = 'uZlzifzY6lLnyyWcbS2pUV1E7qmmq8Li7cG8HvG3vY2tP'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count=10):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {'text': tweet.text, 'sentiment': get_tweet_sentiment(tweet.text)}

                # saving text of tweet
                # saving sentiment of tweet

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def get_ratings(ticker):
    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query=ticker, count=100)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets for {}: {} %".format(ticker, round(100 * len(ptweets) / len(tweets))))
    return round(100 * len(ptweets) / len(tweets))


# # picking negative tweets from tweets
# ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# # percentage of negative tweets
# print("Negative tweets percentage: {} %".format(round(100*len(ntweets)/len(tweets))))
# # percentage of neutral tweets
# print("Neutral tweets percentage: {} % \
# 	".format(round(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))))

# # printing first 5 positive tweets
# print("\n\nPositive tweets:")
# for tweet in ptweets[:10]:
# 	print(tweet['text'])

# # printing first 5 negative tweets
# print("\n\nNegative tweets:")
# for tweet in ntweets[:10]:
# 	print(tweet['text'])

# returns list of new top 50 companies by positivity score
def get_new_50():
    dic = {}
    with open('constituents.txt', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rowcount = 0  # remove this line if testing with all 500
        for row in csv_reader:
            dic[row["Symbol"]] = get_ratings(row["Symbol"])

            # comment this out for full scale testing
            if rowcount < 20:
                rowcount += 1
            else:
                break

    # change list comprehension to [:50] for full scale testing
    return [k for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)[:10]]

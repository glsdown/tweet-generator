import csv
import pickle
import re

import tweepy

from credentials import (
    ACCESS_KEY,
    ACCESS_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET
)


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this
    # method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed
    # count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name,
            count=200,
            max_id=oldest,
            tweet_mode="extended",
        )

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = []
    text_only = []
    for tweet in alltweets:
        if hasattr(tweet, "full_text"):
            outtweets.append(
                [
                    tweet.id_str,
                    tweet.created_at,
                    tweet.full_text,
                    tweet.retweet_count,
                    tweet.favorite_count,
                ]
            )
            text = re.sub(r"http\S+", "", str(tweet.full_text))
            char_list = [
                text[j]
                for j in range(len(text))
                if ord(text[j]) in range(65536)
            ]
            text = ""
            for j in char_list:
                text = text + j
            text_only.append(text)
        elif hasattr(tweet, "text"):
            outtweets.append(
                [
                    tweet.id_str,
                    tweet.created_at,
                    tweet.text,
                    tweet.retweet_count,
                    tweet.favorite_count,
                ]
            )
            text = re.sub(r"http\S+", "", str(tweet.text))
            char_list = [
                text[j]
                for j in range(len(text))
                if ord(text[j]) in range(65536)
            ]
            text = ""
            for j in char_list:
                text = text + j
            text_only.append(text)
        else:
            outtweets.append(
                [
                    tweet.id_str,
                    tweet.created_at,
                    "null",
                    tweet.retweet_count,
                    tweet.favorite_count,
                ]
            )

    # write the csv
    with open("data/{0}_tweets.csv".format(screen_name), "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["id", "created_at", "text", "retweet_count", "favorite_count"]
        )
        writer.writerows(outtweets)

    # pickling the list
    with open("data/{0}_tweets.pkl".format(screen_name), "wb") as f:
        pickle.dump(text_only, f)


if __name__ == "__main__":
    # pass in the username of the account you want to download
    get_all_tweets("realDonaldTrump")

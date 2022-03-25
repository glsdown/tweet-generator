from collections import defaultdict
from pickle import load
from random import random

from nltk import trigrams
from nltk.tokenize import word_tokenize


def generate_trigram_probabilities(tweets):
    """Identify each trigram and the probability of it occuring"""

    # Tokenize each tweet
    tweets_tokenize = []
    for tweet in tweets:
        tweets_tokenize.append(word_tokenize(tweet))

    model = defaultdict(lambda: defaultdict(lambda: 0))

    # count occurrences of each trigram
    for tweet in tweets_tokenize:
        for w1, w2, w3 in trigrams(tweet, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1

    # transform counts to probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count

    return model


def generate_tweet(model):
    """Create a tweet using the probabilities of each trigram occurring"""

    text = [None, None]
    # Initial probability
    prob = 1.0
    chars = 0

    sentence_finished = False

    while not sentence_finished:
        r = random()
        accumulator = 0.0

        for word in model[tuple(text[-2:])].keys():
            accumulator += model[tuple(text[-2:])][word]

            # Update the probability with the conditional probability of the
            # new word
            if accumulator >= r:
                prob *= model[tuple(text[-2:])][word]
                text.append(word)
                break

        # Calculate the number of characters
        if text[-1] is not None:
            chars += len(text[-1]) + 1  # + 1 for space

        # Check if it's too long
        if chars > 140:
            text = [None, None]
            prob = 1.0
            chars = 0
        # Check if end of tweet reached
        elif text[-2:] == [None, None]:
            sentence_finished = True

    tweet = " ".join([t for t in text if t])

    return prob, tweet


def load_tweets(screen_name):
    """Load the data and create the trigram probability model"""
    # Load data
    with open("data/{0}_tweets.pkl".format(screen_name), "rb") as f:
        tweets = load(f)

    # Identify the trigrams and their respective probabilities
    model = generate_trigram_probabilities(tweets)
    return model


def get_probable_tweet(model):
    """Generate a 'likely' tweet using the trigram model"""
    max = 0
    big_tweet = ""
    # Look at 100 different options and see which the most likely of them is
    for _ in range(100):
        prob, tweet = generate_tweet(model)
        if prob > max:
            big_tweet = tweet

    return big_tweet


if __name__ == "__main__":
    screen_name = "realDonaldTrump"
    print("Generating a tweet for {0}".format(screen_name))
    print(get_probable_tweet(load_tweets(screen_name)))

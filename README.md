# Tweet Generator

This was a project from 2018 where I explored how to generate text using trigrams, by exporting tweets from Twitter, using nltk to tokenize and identify trigrams, then to generate likely Tweets from the outcomes.

It uses the [tweepy library](https://github.com/tweepy/tweepy) to scrape tweets from Twitter. Due to his notoriety on Twitter at the time, it was targetted at Trump's tweets, but could be extended to use any alternative Twitter handle.

It was an exploratory project so is very rough and ready.

## Usage

As this was built a number of years ago, it uses an old method of authentication to scrape tweets from Twitter. To use it, you will need some Twitter credentials stored in a file called `.env`. Whilst this isn't a tutorial I used in this project, there are some good instructions on how to get these [here](https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials).

```python
# .env

# Twitter API credentials
CONSUMER_KEY = "......"
CONSUMER_SECRET = "......"
ACCESS_KEY = "......"
ACCESS_SECRET = "......"
```

You can then run the Twitter bot on the account of your choice by changing the line at the bottom:

```python
# get_trump_tweets.py

if __name__ == "__main__":
    # pass in the username of the account you want to download
    get_all_tweets("realDonaldTrump")
```

Once you have the Tweets scraped and stored in a file in the `data` sub-folder, you can run the tweet generator via the command line using the `tweet_generator` file. Again, you can specify which account to use at the bottom of the file:

```python
# tweet_generator.py

if __name__ == "__main__":
    screen_name = "realDonaldTrump"
    ...
```

If you want to try it out using the GUI, then similarly, you can run this using the `tweet_gui` file; specifying the account to use at the bottom of the page:

```python
# tweet_gui.py

if __name__ == "__main__":
    TweetWindow(screen_name="realDonaldTrump").mainloop()
```
#!/usr/bin/env python3
"""Tweet Floating City"""

import os

import tweepy

from tweetify import tweetify


# pylint: disable=too-few-public-methods
class Twitter:
    """Wrapper for the Twitter API"""

    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(os.environ["API_KEY"],
                                   os.environ["API_SECRET"])
        auth.set_access_token(os.environ["ACCESS_TOKEN"],
                              os.environ["ACCESS_TOKEN_SECRET"])
        self._api = tweepy.API(auth, wait_on_rate_limit=True)

    def last_status_text(self) -> str:
        """Get the most recent status, if it exists"""
        user = self._api.verify_credentials(include_entities=False,
                                            tweet_mode="extended")
        try:
            return user.status.full_text
        except AttributeError:
            return None

    def update(self, status: str) -> tweepy.models.Status:
        """Post tweet"""
        return self._api.update_status(status=status)


def main() -> None:
    """Entry point"""
    twitter = Twitter()

    last_tweet = twitter.last_status_text()
    future_tweets = tweetify("data/floating_city.md")

    try:
        next_tweet_index = future_tweets.index(last_tweet) + 1
        # next_tweet_index %= len(future_tweets)  # Just stop instead.
    except ValueError:
        # There was no last_tweet
        next_tweet_index = 0

    if next_tweet_index >= len(future_tweets):
        print("EOF")
        return

    status = future_tweets[next_tweet_index]
    print(status)
    twitter.update(status)

if __name__ == "__main__":
    main()

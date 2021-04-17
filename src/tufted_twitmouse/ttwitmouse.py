import tweepy
import asyncio
import json


class TTwitmouse:
    def __init__(self, keyfile, user_id, config_file=None):
        """
        Initializes the TTwitmouse follower
        keyfile: the file containing a Twitter API key and secret
        user_id: the id of the user to follow
        config_file: the name of a config file to load, defaults to None
        """
        with open(keyfile, 'r') as kf:
            key, secret = kf.readlines()
            key = key.strip()
            secret = secret.strip()
        auth = tweepy.AppAuthHandler(key, secret)
        self.api = tweepy.API(auth)
        self._uid = user_id
        if config_file is None:
            self.oldest_tweet = None
        else:
            with open(config_file, 'r') as cf:
                # For now; the config file only contains the ID of the user's
                # oldest tweet. It might contain more in the future.
                self.oldest_tweet = cf.read()
                self.oldest_tweet = self.oldest_tweet.strip()

    async def get_tweets(self):
        """
        If there is no saved configuration, gets N tweets from the followed
        user. N is defined somewhere in the Twitter API.
        If there *is* a saved configuration; gets *up to* N tweets from the
        followed user, stopping at the tweet *after* the oldest tweet.
        """
        if self.oldest_tweet:
            tweets = self.api.user_timeline(self._uid, tweet_mode="extended",
                                            since_id=self.oldest_tweet,
                                            include_rts=False)
        else:
            tweets = self.api.user_timeline(self._uid, tweet_mode="extended",
                                            include_rts=False)
        if tweets:
            self.oldest_tweet = tweets[0].id
        return tweets

    async def watch(self, queue, interval=1800, until=None):
        """
        Polls the Twitter API for new tweets from the specified user every
        `interval` until `until` and yields the results.
        interval: how ofter to retreive tweets, default is 1800s, or 15min
        until: a function that returns a Boolean value
        """
        if until is None:
            def condition():
                return True
        else:
            condition = until
        while(condition()):
            await queue.put(await self.get_tweets())
            await asyncio.sleep(interval)

    async def listen_for(self, term, queue, interval=1800, until=None):
        tweet_queue = asyncio.Queue()
        watcher = asyncio.create_task(self.watch(tweet_queue, interval, until))
        while True:
            tweets_to_grok = await tweet_queue.get()
            tweets = []
            for tweet in tweets_to_grok:
                if term in tweet._json['full_text']:
                    tweets.append(tweet)
            await queue.put(tweets)
        await tweet_queue.join()
        await asyncio.gather(watcher)

import tweepy
import json
import asyncio


class TTwitmouse:
    def __init__(self, keyfile, user_id):
        with open(keyfile, 'r') as kf:
            key, secret = kf.readlines()
            key = key.strip()
            secret = secret.strip()
        auth = tweepy.AppAuthHandler(key, secret)
        self.api = tweepy.API(auth)
        self._uid = user_id
        self.oldest_tweet = None


    def get_tweets(self):
        if self.oldest_tweet:
            return self.api.user_timeline(self._uid, tweet_mode="extended",
                                          since_id=self.oldest_tweet.id,
                                          include_rts=False)
        else:
            return self.api.user_timeline(self._uid, tweet_mode="extended", 
                                          include_rts=False)



if __name__ == "__main__":
    async def test_function():
        keyfile = 'twitter_api_key'
        user_to_poll = TTwitmouse(keyfile, '4083387437')
        tweets = user_to_poll.get_tweets()
        for tweet in tweets:
            print(tweet.full_text)


    asyncio.run(test_function())
    

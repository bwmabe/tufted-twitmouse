import asyncio
from ttwitmouse import TTwitmouse


async def main():
    ttmouse = TTwitmouse('twitter_api_key', '3160892443')
    queue = asyncio.Queue()
    tweet_getter = asyncio.create_task(ttmouse.listen_for("#GTAOnline", queue, interval=30))
    while True:
        tweets = await queue.get()
        for tweet in tweets:
            print(tweet.full_text, end="\n---\n")
    await queue.join()
    await asyncio.gather(tweet_getter)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

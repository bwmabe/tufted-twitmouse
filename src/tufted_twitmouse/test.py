import asyncio
from ttwitmouse import TTwitmouse


async def main():
    ttmouse = TTwitmouse('twitter_api_key', '150621067')
    queue = asyncio.Queue()
    tweet_getter = asyncio.create_task(ttmouse.watch(queue, interval=30))
    try:
        while True:
            tweets = await queue.get()
            for tweet in tweets:
                print(tweet)
    except Exception as e:
        print(e)
    await queue.join()
    await asyncio.gather(tweet_getter)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

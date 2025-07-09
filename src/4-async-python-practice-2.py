import asyncio
import datetime

async def background_worker():
    for i in range(10):
        print(f"{datetime.datetime.now().time()}: Working... step {i}")
        await asyncio.sleep(1)

async def main():
    task = asyncio.create_task(background_worker())
    print(f"{datetime.datetime.now().time()}: the main wants to sleep for 5 seconds")
    await asyncio.sleep(5)
    print(f"{datetime.datetime.now().time()}: Now waiting for the worker to finish.")
    await task
    print(f"{datetime.datetime.now().time()}: The task is finished")

asyncio.run(main())
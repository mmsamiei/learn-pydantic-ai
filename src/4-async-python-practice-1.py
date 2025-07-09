import asyncio
import datetime
import time
import random

import config

async def greet(name):
    time_to_sleep = random.randint(1, 5)
    print(f"{datetime.datetime.now().time()}: Hello, {name}! sleep {time_to_sleep} seconds")
    config = ['time.sleep', 'asyncio.sleep', 'await asyncio.sleep'][2]
    if config == 'time.sleep':
        time.sleep(time_to_sleep)
    elif config == 'asyncio.sleep':
        asyncio.sleep(time_to_sleep)
    elif config == 'await asyncio.sleep':
        await asyncio.sleep(time_to_sleep)
    print(f"{datetime.datetime.now().time()}: Goodbye, {name}!")

async def main():
    await asyncio.gather(
        greet("Ali"),
        greet("Bahram"),
        greet("Chakameh"),
        greet("Davood"),
        greet("Ehsan"),
    )
    

asyncio.run(main())

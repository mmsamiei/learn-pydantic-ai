import random
import time
import asyncio
from tqdm.asyncio import trange, tqdm

WHEAT_TIME = 1
FLOUR_TIME = 3
BREAD_TIME = 2

async def wheat_producer(wheat_queue):
    """Producer that generates wheat and puts it in the queue"""
    for i in range(100):
        wheat = i
        print(f"Produced wheat {wheat}")
        await wheat_queue.put(wheat)
        await asyncio.sleep(WHEAT_TIME)
    await wheat_queue.put(None)  # Signal end of production

async def flour_producer(wheat_queue, flour_queue):
    """Consumer of wheat, producer of flour"""
    while True:
        wheat = await wheat_queue.get()
        if wheat is None:  # End signal
            await flour_queue.put(None)
            break
        flour = wheat
        print(f"Produced flour {flour}")
        await flour_queue.put(flour)
        await asyncio.sleep(FLOUR_TIME)

async def bread_producer(flour_queue, bread_queue):
    """Consumer of flour, producer of bread"""
    while True:
        flour = await flour_queue.get()
        if flour is None:  # End signal
            await bread_queue.put(None)
            break
        bread = flour 
        print(f"Produced bread {bread}")
        await bread_queue.put(bread)
        await asyncio.sleep(BREAD_TIME)

async def bread_consumer(bread_queue):
    """Final consumer that collects all bread"""
    breads = []
    while True:
        bread = await bread_queue.get()
        if bread is None:  # End signal
            break
        breads.append(bread)
    return breads

async def main():
    # Create queues for communication between producers/consumers
    wheat_queue = asyncio.Queue()
    flour_queue = asyncio.Queue()
    bread_queue = asyncio.Queue()
    
    start_time = time.time()
    
    # Create and run all tasks concurrently
    tasks = [
        wheat_producer(wheat_queue),
        flour_producer(wheat_queue, flour_queue),
        bread_producer(flour_queue, bread_queue),
        bread_consumer(bread_queue)
    ]
    
    # Wait for all tasks to complete and get the final result
    results = await asyncio.gather(*tasks)
    breads = results[-1]  # bread_consumer returns the list of breads
    
    end_time = time.time()
    print(f"Time: {end_time - start_time}")
    print(f"Total breads produced: {len(breads)}")

# Run the async main function
asyncio.run(main())

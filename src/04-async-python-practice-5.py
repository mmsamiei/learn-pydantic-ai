import asyncio
import datetime
import random

async def worker(worker_id, task):
    delay = random.uniform(5, 20)  # Simulate different response times
    print(f"{datetime.datetime.now().time()}: Worker {worker_id} is starting the task, delay {delay:.2f} seconds")
    await asyncio.sleep(delay)
    
    # Simulate potential errors in workers
    if random.random() < 0.6:  # 20% chance of error
        print(f"{datetime.datetime.now().time()}: Worker {worker_id} encountered an error!")
        raise Exception(f"Worker {worker_id} failed to process the task")
    
    result = f"Result from worker {worker_id}: {task.upper()}"
    print(f"{datetime.datetime.now().time()}: Worker {worker_id} finished the task")
    return result

async def main():
    task_description = "Process this data"
    
    # Create tasks for each worker
    worker_names = [
        'Ali', 'Bahram', 'Chakameh', 'Davood', 'Ehsan',
        'Farhad', 'Gisoo', 'Hassan', 'Javad', 'Kambiz'
    ]

    tasks = [asyncio.create_task(worker(name, task_description)) for name in worker_names]
    
    while tasks:
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
            timeout=15
        )

        for task in done:
            try:
                fastest_result = await task  # Get the result or exception
                print(f"{datetime.datetime.now().time()}: Fastest result: {fastest_result}")
                
                # Cancel the remaining tasks
                for task in pending:
                    task.cancel()
                    print(f"{datetime.datetime.now().time()}: Canceled a pending task")
                return  # Exit the loop after getting a valid result
            except Exception as e:
                print(f"{datetime.datetime.now().time()}: Task raised an exception: {e}")
                tasks.remove(task)  # Remove the failed task from the list
                
        if not done:
            print(f"{datetime.datetime.now().time()}: Timeout occurred, no worker finished in time.")
            # Cancel the remaining tasks
            for task in pending:
                task.cancel()
                print(f"{datetime.datetime.now().time()}: Canceled a pending task")
            return

asyncio.run(main())
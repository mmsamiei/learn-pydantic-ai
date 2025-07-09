import asyncio
import datetime
import random

async def worker(worker_id, task):
    delay = random.uniform(5, 15)  # Simulate different response times
    print(f"{datetime.datetime.now().time()}: Worker {worker_id} is starting the task, delay {delay:.2f} seconds")
    await asyncio.sleep(delay)
    result = f"Result from worker {worker_id}: {task.upper()}"
    print(f"{datetime.datetime.now().time()}: Worker {worker_id} finished the task")
    return result

async def main():
    task_description = "Process this data"
    
    # Create tasks for each worker
    worker1_task = worker('Ali', task_description)
    worker2_task = worker('Bahram', task_description)
    worker3_task = worker('Chakameh', task_description)

    # Use asyncio.wait to get the fastest result
    done, pending = await asyncio.wait(
        [worker1_task, worker2_task, worker3_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    print(f"{datetime.datetime.now().time()}: one of the workers finished the task")

    # Get the result from the first completed task
    fastest_result = done.pop().result()
    print(f"{datetime.datetime.now().time()}: Fastest result: {fastest_result}")

    # Cancel the remaining tasks
    for task in pending:
        task.cancel()
        print(f"{datetime.datetime.now().time()}: Canceled a pending task")

asyncio.run(main())
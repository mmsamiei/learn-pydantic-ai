import os
import sys
import asyncio

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
import datetime

import logging
logging.basicConfig(level=logging.INFO)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

agent_gemini1 = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)))
agent_gemini2 = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)))
agent_gemini3 = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)))


async def main():
    
    task_description = "count to 133"
    
    # Create tasks for each agent
    gemini_task1 = asyncio.create_task(agent_gemini1.run(task_description))
    gemini_task2 = asyncio.create_task(agent_gemini2.run(task_description))
    gemini_task3 = asyncio.create_task(agent_gemini3.run(task_description))

    tasks = [gemini_task1, gemini_task2, gemini_task3]
    
    
    while tasks:
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
            timeout=15
        )
        for task in done:
            try:
                fastest_result = await task  # Get the result or exception
                if task is gemini_task1:
                    fastest_agent = "Gemini 1"
                elif task is gemini_task2:
                    fastest_agent = "Gemini 2"
                else:
                    fastest_agent = "Gemini 3"
                logging.info(f"{datetime.datetime.now().time()}: {fastest_agent} finished the task")
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

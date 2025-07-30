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

agent_openai = Agent(model=OpenAIModel('gpt-4o-mini', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)))
agent_gemini = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)))


async def main():
    
    task_description = "What is the capital of France?"
    
    # Create tasks for each agent
    openai_task = asyncio.create_task(agent_openai.run(task_description))
    gemini_task = asyncio.create_task(agent_gemini.run(task_description))

    # Use asyncio.wait to get the fastest result
    done, pending = await asyncio.wait(
        [openai_task, gemini_task],
        return_when=asyncio.FIRST_COMPLETED,
        timeout=7
    )

    if done:
        print(f"{datetime.datetime.now().time()}: one of the agents finished the task")
        
        fastest_task = done.pop()
        fastest_result = fastest_task.result()

        if fastest_task is openai_task:
            fastest_agent = "OpenAI"
        else:
            fastest_agent = "Gemini"
        print(f"{datetime.datetime.now().time()}: Fastest result: {fastest_result} from {fastest_agent}")
    else:
        print(f"{datetime.datetime.now().time()}: Timeout occurred, no agent finished in time.")
        fastest_result = None
        fastest_agent = None

    # Cancel the remaining tasks
    for task in pending:
        task.cancel()
        print(f"{datetime.datetime.now().time()}: Canceled a pending task")

    

asyncio.run(main())

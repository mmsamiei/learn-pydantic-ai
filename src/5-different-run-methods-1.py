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

model = OpenAIModel(
    'gpt-4o-mini',
    provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY),
)
agent = Agent(model=model)
result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.output)

async def main():
    result = await agent.run('What is the capital of France?')
    print(result.output)
    # gather all the results
    
    logging.info(f"{datetime.datetime.now().time()}: Gathering all the results")
    results = await asyncio.gather(
        agent.run('What is the capital of France? who is the president of France?'),
        agent.run('What is the capital of Italy? who is the president of Italy?'),
        agent.run('What is the capital of Germany? who is the president of Germany?'),
        agent.run('What is the capital of Spain? who is the president of Spain?'),
        agent.run('What is the capital of Portugal? who is the president of Portugal?'),
        agent.run('What is the capital of Greece? who is the president of Greece?'),
        agent.run('What is the capital of Turkey? who is the president of Turkey?'),
    )
    logging.info(f"{datetime.datetime.now().time()}: Results: {results}")

asyncio.run(main())

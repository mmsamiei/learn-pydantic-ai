import os
import sys
import asyncio

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from datetime import date


import logging
logging.basicConfig(level=logging.INFO)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

agent_gemini = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)), instructions="Use the name of user while replying", deps_type=str)


@agent_gemini.instructions  
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}."


@agent_gemini.instructions
def add_the_date() -> str:  
    return f'The date is {date.today()}.'

result = agent_gemini.run_sync('What is the date?', deps='Frank')
print(result)
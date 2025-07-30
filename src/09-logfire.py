import os
import sys

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

import logfire

logfire.configure()  
logfire.instrument_pydantic_ai()  


model = OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(
            base_url=API_URL, api_key=API_KEY
        ),
    )
agent = Agent(model=model, instructions='Be concise, reply with one sentence.')
result = agent.run_sync('Where does "hello world" come from?')  
print(result.output)
"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""
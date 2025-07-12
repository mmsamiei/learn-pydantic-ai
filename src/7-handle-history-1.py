import os
import sys
import asyncio

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from datetime import date
from pydantic_core import to_jsonable_python
from pydantic_ai.messages import ModelMessagesTypeAdapter  

import logging
logging.basicConfig(level=logging.INFO)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

agent_gemini = Agent(model=OpenAIModel('gemini-2.0-flash', provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY)), instructions="Use the name of user while replying", deps_type=str)

result1 = agent_gemini.run_sync('Tell me a joke.')
history_step_1 = result1.all_messages()
as_python_objects = to_jsonable_python(history_step_1)  
same_history_as_step_1 = ModelMessagesTypeAdapter.validate_python(as_python_objects)

result2 = agent_gemini.run_sync(  
    'Tell me a different joke.', message_history=same_history_as_step_1
)

# WARNING: Manually building message history is generally not recommended,
#          but it can be helpful for understanding message structure.
#          This is a manual example of how to build a message history.  

import os
import sys
import asyncio
import logging
import json
from datetime import date

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_core import to_jsonable_python
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_ai.messages import ModelMessage
from pydantic_ai.messages import ModelMessagesTypeAdapter  

from pprint import pprint

logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

agent_gemini = Agent(
    model=OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY),
    ),
    system_prompt='the system prompt says you are a sad joke teller',
    instructions='static instructions: You are a funny joke teller.',
)

@agent_gemini.instructions
def add_the_date() -> str:  
    return f'The date is {date.today()}.'

result1 = agent_gemini.run_sync('Tell me a joke about a cat.')

# Convert to Python dict and print with nice formatting
messages_data = result1.all_messages_json()

# Parse JSON string to Python object and pretty print
print('-------------------------')
messages_json = json.loads(messages_data.decode('utf-8'))
print(json.dumps(messages_json, indent=2))

history_manual_json = [
  {
    "parts": [
      {
        "content": "Tell me a joke.",
        # "timestamp": "2025-07-12T14:53:44.673706Z",
        "part_kind": "user-prompt"
      }
    ],
    "instructions": None,
    "kind": "request"
  },
  {
    "parts": [
      {
        "content": "Why don't scientists trust atoms?\n\nBecause they make up everything!\n",
        "part_kind": "text"
      }
    ],
    # "usage": {
    #   "requests": 1,
    #   "request_tokens": 5,
    #   "response_tokens": 16,
    #   "total_tokens": 21,
    #   "details": {}
    # },
    # "model_name": "gemini-2.0-flash",
    # "timestamp": "2025-07-12T14:53:45Z",
    "kind": "response",
    # "vendor_details": None,
    # "vendor_id": "-XZyaJHFG5WhhMIP_MPhmAY"
  }
]

print('-------------------------')
history_manual_python = ModelMessagesTypeAdapter.validate_python(history_manual_json)
result2a = agent_gemini.run_sync('what was your last joke about?.', message_history=history_manual_python)
messages_data = result2a.all_messages_json()
messages_json = json.loads(messages_data.decode('utf-8'))
print(json.dumps(messages_json, indent=2))

print('-------------------------')
result2b = agent_gemini.run_sync('what was your last joke about?.', message_history=result1.all_messages())
messages_data = result2b.all_messages_json()
messages_json = json.loads(messages_data.decode('utf-8'))
print(len(messages_json))
print(json.dumps(messages_json, indent=2))


# Pydantic-AI When you give it message history and instructions, ignore instruction of message history.
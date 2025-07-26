# WARNING: Manually building message history is generally not recommended,
#          but it can be helpful for understanding message structure.
#          This is a manual example of how to build a message history.  

import os
import sys
import asyncio
import logging
import json
from datetime import date

from pydantic_ai import Agent, RunContext
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


plain_text = """
Emma Tehrani is a 10 years old girl.
Emma gets 15 marks in math.
Emma gets 10 marks in science.
Jack Rashti is a 13 years old boy.
Jack gets 12 marks in math.
Jack gets 14 marks in english.
Fatemeh Tamehri is a 20 years old girl.
Fatemeh Tamehri gets 0 marks in math.
Fatemeh Tamehri gets 2 marks in computer.
Fatemeh Tamehri gets 2 point less than emma in science.
Ali Rezaei is a 15 years old boy.
Ali Rezaei gets 10 marks in math.
Ali Rezaei gets 12 marks in science.
Ali Rezaei gets 14 marks in english.
Ali Rezaei gets 16 marks in computer.
Ali Rezaei gets 18 marks in history.
Ali Rezaei gets 20 marks in geography.
"""

gemini_model = OpenAIModel(
    'gemini-2.0-flash',
    provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY),
)

retrieval_agent = Agent(
    model=gemini_model,
    instructions="you should retrieve the sentences that are relevant to the user's query.",
    output_type=list[str]
)

@retrieval_agent.tool
async def retrieve_documents(ctx: RunContext, query: str) -> str:
    """return all sentences that may be relevant to the user's query."""
    return plain_text

generation_agent = Agent(
    model=gemini_model,
    instructions=f"you should answer the user's query based on the retrieved documents. at the end of your answer, you should say 'the date is {date.today()}.'"
)

@generation_agent.tool
async def retrieve_documents(ctx: RunContext, inquery: str) -> str:
  result = await retrieval_agent.run(inquery)
  logging.info(f"retrieved documents: {result}")
  return result

result = generation_agent.run_sync('what is the average marks of Tamehri?')
print(result)

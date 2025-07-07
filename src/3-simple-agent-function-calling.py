import os 
import sys

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

async def count_number_of_words(text: str) -> int:
    return len(text.split())

print("Starting simple agent with structured output...")

try:
    model = OpenAIModel(
        'gpt-4o-mini',
        provider=OpenAIProvider(
            base_url=API_URL, api_key=API_KEY
        ),
    )
    agent = Agent(model=model, output_type=count_number_of_words, system_prompt="You are a helpful assistant that counts the number of words in a text")
    response = agent.run_sync("Hello I am Mahdi, I am 28 years old")
    print("Agent's response:", response)

except Exception as e:
    print(f"An error occurred: {e}")

print("Simple agent with structured output finished.")
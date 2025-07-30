import os 
import sys

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

class Country(BaseModel):
    name: str
    capital: str
    population: int
    president: str

class State(BaseModel):
    name: str
    capital: str
    population: int
    governor: str
    

print("Starting simple agent with structured output...")

try:
    model = OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(
            base_url=API_URL, api_key=API_KEY
        ),
    )
    agent = Agent(model=model, output_type=list[Country, State])
    response = agent.run_sync("write 5 random countries or states of USA")
    print("Agent's response:", response)

except Exception as e:
    print(f"An error occurred: {e}")

print("Simple agent with structured output finished.")
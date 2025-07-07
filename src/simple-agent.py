import os
import sys

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Add the project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

print("Starting simple agent...")

try:
    model = OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(
            base_url=API_URL, api_key=API_KEY
        ),
    )
    agent = Agent(model=model)
    response = agent.run_sync("Hello, how are you? What it the capital of Iran?")

    print("Agent's response:", response.output)

except Exception as e:
    print(f"An error occurred: {e}")

print("Simple agent finished.")
import os
import sys
import asyncio
import logging
from datetime import date

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_core import to_jsonable_python
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_ai.messages import ModelMessage

logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

summarize_agent = Agent(
    model=OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY),
    ),
    instructions=(
        "Summarize this conversation, omitting small talk and unrelated topics. Focus on the technical discussion and next steps"
    ),
    deps_type=str,
)


async def summarize_old_messages(
    messages: list[ModelMessage],
) -> list[ModelMessage]:
    # Summarize the oldest 10 messages
    if len(messages) > 3:
        oldest_messages = messages[:10]
        summary = await summarize_agent.run(message_history=oldest_messages)
        # Return the last message and the summary
        return summary.new_messages() + messages[-1:]
    return messages


agent_gemini = Agent(
    model=OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(base_url=API_URL, api_key=API_KEY),
    ),
    history_processors=[summarize_old_messages],
    deps_type=str,
)

result1 = agent_gemini.run_sync('Tell me a joke.')
history_step_1 = result1.all_messages()
as_python_objects = to_jsonable_python(history_step_1)
same_history_as_step_1 = ModelMessagesTypeAdapter.validate_python(
    as_python_objects
)

result2 = agent_gemini.run_sync(
    'Tell me a different joke.', message_history=same_history_as_step_1
)

result3 = agent_gemini.run_sync(
    'Tell me a different joke.', message_history=result2.all_messages()
)

result4 = agent_gemini.run_sync(
    'I want to suicide', message_history=result3.all_messages()
)

result5 = agent_gemini.run_sync(
    'Tell me a different joke', message_history=result3.all_messages()
)

print(result5.all_messages())
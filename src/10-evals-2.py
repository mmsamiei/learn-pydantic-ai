import os
import sys


from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent, format_as_xml
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import IsInstance, LLMJudge


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from config import API_KEY, API_URL

model = OpenAIModel(
        'gemini-2.0-flash',
        provider=OpenAIProvider(
            base_url=API_URL, api_key=API_KEY
        ),
    )

class Recipe(BaseModel):
    ingredients: list[str]
    steps: list[str]

agent = Agent(
    model=model, 
    instructions='Generate a recipe to cook the dish that meets the dietary restrictions.',
    output_type=Recipe,
)

class CustomerOrder(BaseModel):  
    dish_name: str
    dietary_restriction: str | None = None

async def transform_recipe(customer_order: CustomerOrder) -> Recipe:  
    r = await agent.run(format_as_xml(customer_order))
    return r.output

recipe_dataset = Dataset[CustomerOrder, Recipe, Any](  
    cases=[
        Case(
            name='vegetarian_recipe',
            inputs=CustomerOrder(
                dish_name='Spaghetti Bolognese', dietary_restriction='vegetarian'
            ),
            expected_output=None,  # 
            metadata={'focus': 'vegetarian'},
            evaluators=(
                LLMJudge(  
                    rubric='Recipe should not contain meat or animal products',
                    model=model,
                ),
            ),
        ),
        Case(
            name='gluten_free_recipe',
            inputs=CustomerOrder(
                dish_name='Chocolate Cake', dietary_restriction='gluten-free'
            ),
            expected_output=None,
            metadata={'focus': 'gluten-free'},
            # Case-specific evaluator with a focused rubric
            evaluators=(
                LLMJudge(
                    rubric='Recipe should not contain gluten or wheat products',
                    model=model,
                ),
            ),
        ),
        Case(
            name='vegan_recipe',
            inputs=CustomerOrder(
                dish_name='قیمه گوشتی',
            ),
            expected_output=None,
            evaluators=(
                LLMJudge(
                    rubric='Recipe should not contain meat',
                    model=model,
                ),
            ),
        ),
    ],
    evaluators=[  
        IsInstance(type_name='Recipe'),
        LLMJudge(
            rubric='Recipe should have clear steps and relevant ingredients',
            include_input=True,
            model=model,  
        ),
    ],
)

report = recipe_dataset.evaluate_sync(transform_recipe)
print(report)
from google.adk.agents import SequentialAgent
from dotenv import load_dotenv

from .sub_agents.greet_select_dish import greet_select_dish
from .sub_agents.list_ingredients import list_ingredients
from .sub_agents.cooking_guide import cooking_guide

load_dotenv()

root_agent = SequentialAgent(
    name="recipe_agent",
    description="A Recipe Agent that Greets and Selects dish, lists ingredients, give step by step cooking guide to the user",
    sub_agents=[greet_select_dish, list_ingredients, cooking_guide],
)

from google.adk.agents import Agent

list_ingredients = Agent(
    name="list_ingredients",
    model="gemini-2.5-flash",
    description="Ingredients List Agent",
    instruction="""
        You are an Ingredients Listing Agent.
        You job is to recognize the dish name that user mentioned and list out all the ingredients of it.

        Example output:
        [ingredient 1, ingredient 2, ingredient 3, ...]
    """,
    output_key="ingredients_list",
)

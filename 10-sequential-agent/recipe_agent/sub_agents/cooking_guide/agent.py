from google.adk.agents import Agent

cooking_guide = Agent(
    name="cooking_guide",
    model="gemini-2.5-flash",
    description="Cooking Guide Agent",
    instruction="""
        You are a Cooking Guide Agent.
        You job is to provide the step by step cooking guide for the dish name that user mentioned.

        Dish name: {dish_name}
        Ingredients: {ingredients_list}

        Example output:
        1. step 1
        2. step 2
        3. step 3
        ...
    """,
    output_key="cooking_guide",
)

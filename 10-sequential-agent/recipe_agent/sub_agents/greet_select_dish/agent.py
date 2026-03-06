from google.adk.agents import Agent

greet_select_dish = Agent(
    name="greet_select_dish",
    model="gemini-2.5-flash",
    description="Agent that Greets the User and Selects the Dish",
    instruction="""
    You are a Greet and Dish selector agent.
    You need to greet the user initially.
    And if user mentions a Dish name you need to give response that dish name.

    Examples:
        User: Hello
        Agent: Hello, What Dish you want to select

        User: How to cook Chicken Biriyani
        Agent: Chicken Biriyani
    """,
    output_key="dish_name",
)

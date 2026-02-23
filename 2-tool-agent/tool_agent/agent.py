from google.adk.agents import Agent


# --- Built-in google_search Tool ---
from google.adk.tools import google_search
root_agent = Agent(
    name="tool_agent",
    model="gemini-2.5-flash",
    description="Tool Agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search], # We can only use one tool at a time
)



# --- Custom Function 'get_current_time' Tool ---
# from datetime import datetime
# # Make sure not to add any default parameters
# def get_current_time(format: str) -> dict:
#     # Make sure to specify proper DocString
#     """
#     Get the current time in the format DD-MM-YYYY HH-MM-SS
#     """
    
#     # Make sure to always return a dict object
#     return {
#         "current_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
#     }
    
# root_agent = Agent(
#     name="tool_agent",
#     model="gemini-2.5-flash",
#     description="Tool Agent",
#     instruction="""
#     You are a helpful assistant that can use the following tools:
#     - get_current_time
    
#     """,
#     tools=[get_current_time], # We can only use one tool at a time
# )
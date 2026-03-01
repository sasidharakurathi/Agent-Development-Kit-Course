from hashlib import new
from google.genai import types
from google.adk.runners import Runner


def get_initial_state(user_name: str) -> dict:
    return {
        "user_name": user_name,
        "reminders": [],
    }


async def call_agent_async(runner: Runner, user_id, session_id, user_input):

    message = types.Content(parts=[types.Part(text=str(user_input))])

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Response: {event.content.parts[0].text}")

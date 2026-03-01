import uuid

from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from question_answering_agent import question_answering_agent
from google.genai import types

import asyncio


async def main():

    load_dotenv()

    session_service_stateful = InMemorySessionService()

    app_name = "Pratice App"
    user_id = "Sasidhar"
    session_id = str(uuid.uuid4())

    initial_state = {
        "user_name": "Sasidhar",
        "user_preferences": """
            Enjoys playing cricket and video games.
            Works as a Software Engineer / AI Engineer.
            Loves researching new technologies and Artificial Intelligence.
            Hobbies include listening to music and building projects.
        """
    }

    await session_service_stateful.create_session(
        app_name=app_name, user_id=user_id, state=initial_state, session_id=session_id
    )

    runner = Runner(
        app_name=app_name,
        agent=question_answering_agent,
        session_service=session_service_stateful,
    )

    new_message = types.Content(parts=[types.Part("What's the user name?")])

    for event in runner.run(
        user_id=user_id, session_id=session_id, new_message=new_message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    session = await session_service_stateful.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())

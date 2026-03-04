import asyncio

from customer_service_agent.agent import customer_service_agent

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import add_user_query_to_history, call_agent_async, get_initial_state

import uuid

load_dotenv()


app_name = "Customer Support"
database_url = "sqlite+aiosqlite:///./my_agent_data.db"


async def main():

    database_session_service = DatabaseSessionService(db_url=database_url)

    print(f"--- Welcome to Customer Support Agent ---")
    user_name = input("Enter your name: ")
    user_id = user_name.strip().replace(" ", "_")

    existing_sessions = await database_session_service.list_sessions(
        app_name=app_name, user_id=user_id
    )

    if existing_sessions and existing_sessions.sessions:
        session_id = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {session_id}")

    else:

        session_id = str(uuid.uuid4())
        initial_state = get_initial_state(user_name)

        await database_session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state=initial_state,
            session_id=session_id,
        )

        print(f"Created new session: {session_id}")

    runner = Runner(
        agent=customer_service_agent,
        app_name=app_name,
        session_service=database_session_service,
    )

    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break
        await add_user_query_to_history(
            database_session_service, app_name, user_id, session_id, user_input
        )

        await call_agent_async(runner, user_id, session_id, user_input)

    final_session = await database_session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())

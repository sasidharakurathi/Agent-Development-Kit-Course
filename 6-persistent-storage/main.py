import uuid
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from memory_agent import memory_agent
from dotenv import load_dotenv
import asyncio
from utils import get_initial_state, call_agent_async

app_name = "Memory Agent"
database_url = "sqlite+aiosqlite:///./my_agent_data.db"


async def main():

    load_dotenv()

    database_session_service = DatabaseSessionService(database_url)

    print(f"--- Welcome to Memory Agent ---")
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
        app_name=app_name,
        agent=memory_agent,
        session_service=database_session_service,
    )

    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break

        await call_agent_async(runner, user_id, session_id, user_input)


if __name__ == "__main__":
    asyncio.run(main())

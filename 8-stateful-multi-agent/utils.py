import asyncio
from datetime import datetime
from google.adk.events import Event, EventActions
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types


async def update_interaction_history(
    session_service: DatabaseSessionService,
    author: str,
    app_name: str,
    user_id: str,
    session_id: str,
    entry: dict,
):

    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        interaction_history = session.state.get("interaction_history", [])

        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        interaction_history.append(entry)

        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history

        event = Event(
            invocation_id="history_update",
            author=author,
            actions=EventActions(
                state_delta={"interaction_history": interaction_history}
            ),
        )
        await session_service.append_event(session, event)
    except Exception as e:
        print(f"Error updating interaction history: {e}")


async def add_user_query_to_history(
    session_service: DatabaseSessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    query: str,
):

    await update_interaction_history(
        session_service,
        "user",
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )


async def add_agent_response_to_history(
    session_service: DatabaseSessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    agent_name: str,
    response: str,
):

    await update_interaction_history(
        session_service,
        agent_name,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )


def _suppress_adk_cleanup_errors(loop, context):
    """Suppress the known google-genai aclose() AttributeError noise."""
    exc = context.get("exception")
    if isinstance(exc, AttributeError) and "_async_httpx_client" in str(exc):
        return  # swallow known library bug
    loop.default_exception_handler(context)


async def call_agent_async(
    runner: Runner,
    user_id: str,
    session_id: str,
    query: str,
):
    # Suppress noisy background task errors from the google-genai library.
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(_suppress_adk_cleanup_errors)

    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None
    agent_name = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.author:
                agent_name = event.author

            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                    print(f"Response: {final_response_text}")

    except Exception as e:
        print(f"Agent error: {e}")

    if final_response_text and agent_name:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    return final_response_text


def get_initial_state(user_name: str) -> dict:
    return {
        "user_name": user_name,
        "purchased_courses": [],
        "interaction_history": [],
    }

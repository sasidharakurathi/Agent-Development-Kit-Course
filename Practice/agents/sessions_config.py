from django.conf import settings
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from uuid import uuid4
from typing import Any


def _get_adk_session_service() -> DatabaseSessionService:
    return DatabaseSessionService(db_url=settings.ADK_DB_URL)


def _get_initial_state(user_name: str) -> dict[str, Any]:
    return {
        "user_name": user_name,
        "reminders": [],
    }


async def get_user_session(app_name: str, user_id: str) -> tuple[bool, Any]:
    session_service: DatabaseSessionService = _get_adk_session_service()

    try:
        existing_session = await session_service.list_sessions(
            app_name=app_name, user_id=user_id
        )

        if existing_session and existing_session.sessions:
            return False, existing_session.sessions[0]

        return True, "User Does not exist"
    finally:
        await session_service.close()


async def create_user_session(
    app_name: str, user_name: str, user_id: str
) -> tuple[bool, Any]:
    session_service: DatabaseSessionService = _get_adk_session_service()
    user_session = None

    try:
        user_not_exists, user_session = await get_user_session(app_name, user_id)
        if not user_not_exists:
            return True, "User already exists"

        user_session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state=_get_initial_state(user_name),
            session_id=str(uuid4()),
        )

    finally:
        await session_service.close()

    return False, user_session


def get_runner(app_name: str) -> Runner:
    from reminder_agent import reminder_agent

    return Runner(
        app_name=app_name,
        agent=reminder_agent,
        session_service=_get_adk_session_service(),
    )

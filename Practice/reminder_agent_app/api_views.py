import json
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from agents.sessions_config import get_runner, get_user_session
from .config import APP_NAME
from google.genai import types


@sync_to_async
def _get_user_info(request):
    return request.user.is_authenticated, request.user.username


async def chat(request):
    is_authenticated, user_id = await _get_user_info(request)
    if not is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    error, user_session = await get_user_session(APP_NAME, user_id)
    if error:
        return JsonResponse({"error": f"Session not found: {user_session}"}, status=404)

    session_id = user_session.id

    runner = get_runner(APP_NAME)
    message = types.Content(parts=[types.Part(text=user_message)])

    agent_response = ""

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=message
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    agent_response = event.content.parts[0].text or ""
    finally:
        await runner.session_service.close()

    return JsonResponse(
        {
            "response": agent_response,
        }
    )


async def reminders(request):
    is_authenticated, user_id = await _get_user_info(request)
    if not is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    error, user_session = await get_user_session(APP_NAME, user_id)
    if error:
        return JsonResponse({"reminders": []})

    state = getattr(user_session, "state", {}) or {}
    return JsonResponse({"reminders": state.get("reminders", [])})

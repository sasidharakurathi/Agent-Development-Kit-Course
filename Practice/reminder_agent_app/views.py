from django.shortcuts import render, redirect
from django.http import JsonResponse
from agents.sessions_config import *
from .config import *
from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


async def login(request):

    is_authenticated, user_id = await sync_to_async(
        lambda: (request.user.is_authenticated, request.user.username)
    )()

    if is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # print(f"{request.POST = }")
        user_name = request.POST.get("user_name")
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        error, user_session = await get_user_session(APP_NAME, user_id)

        if error:
            context = {"error": error, "message": user_session}
            return render(request, "reminder_agent/login.html", context)

        error, user = await process_user_login(request, user_id, password)

        if error:
            context = {"error": error, "message": user}
            return render(request, "reminder_agent/login.html", context)

        return redirect("home")

    return render(request, "reminder_agent/login.html")


async def signup(request):

    is_authenticated, user_id = await sync_to_async(
        lambda: (request.user.is_authenticated, request.user.username)
    )()

    if is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # print(f"{request.POST = }")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user_id = request.POST.get("user_id")
        error, user_session = await create_user_session(APP_NAME, user_name, user_id)

        if error:
            context = {"error": error, "message": user_session}
            return render(request, "reminder_agent/signup.html", context)

        error, user = await process_user_signup(request, user_id, password, user_name)

        if error:
            context = {"error": error, "message": user}
            return render(request, "reminder_agent/signup.html", context)

        return redirect("login")

    return render(request, "reminder_agent/signup.html")


async def home(request):

    is_authenticated, user_id = await sync_to_async(
        lambda: (request.user.is_authenticated, request.user.username)
    )()

    if not is_authenticated:
        return redirect("login")

    error, user_session = await get_user_session(APP_NAME, user_id)

    display_name = user_id
    reminders = []

    if not error:
        state = getattr(user_session, "state", {}) or {}
        display_name = state.get("user_name", user_id)
        reminders = state.get("reminders", [])

    context = {
        "display_name": display_name,
        "reminders": reminders,
    }
    return render(request, "reminder_agent/home.html", context)


async def logout(request):
    await sync_to_async(auth_logout)(request)
    return redirect("login")


@sync_to_async
def process_user_signup(request, username, password, display_name):
    if User.objects.filter(username=username).exists():
        return True, "That Username is already taken. Please choose another or log in."

    new_user = User.objects.create_user(
        username=username, password=password, first_name=display_name
    )

    auth_login(request, new_user)

    return False, new_user


@sync_to_async
def process_user_login(request, username, password):

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        return False, user

    if User.objects.filter(username=username).exists():
        return True, "Invalid password for this Username."

    return True, "User not found"

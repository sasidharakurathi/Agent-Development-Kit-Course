from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("api/chat/", api_views.chat, name="chat"),
    path("api/reminders/", api_views.reminders, name="reminders"),
    path("logout/", views.logout, name="logout"),
]

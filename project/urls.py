from django.urls import path
from .views import start, login, register, user_page

urlpatterns = [
	path("", start),
	path("login/", login),
	path("register/", register),
	path("user/<int:id>/", user_page),
]
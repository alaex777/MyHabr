from django.urls import path
from .views import start, login, register, user_page, create_article, article

urlpatterns = [
	path("/start/<int:id>", start),
	path("", login),
	path("login/", login),
	path("register/", register),
	path("user/<int:id>/", user_page),
	path("create_article/user/<int:id>", create_article),
	path("article/<int:id>/user/<int:pk>", article),
]
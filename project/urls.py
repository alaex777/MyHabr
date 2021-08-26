from django.urls import path
from .views import start, login, register, user_page, create_article, article, like_article, dislike_article, like_comment, dislike_comment, delete_article, edit_article, delete_comment, edit_comment

urlpatterns = [
	path("start/<int:id>", start),
	path("", login),
	path("login/", login),
	path("register/", register),
	path("user/<int:id>/", user_page),
	path("create_article/user/<int:id>", create_article),
	path("article/<int:id>/user/<int:pk>", article),
	path("like/article/<int:id_ar>/user/<int:id_us>", like_article),
	path("dislike/article/<int:id_ar>/user/<int:id_us>", dislike_article),
	path("like/comment/<int:id_com>/article/<int:id_ar>/user/<int:id_us>", like_comment),
	path("dislike/comment/<int:id_com>/article/<int:id_ar>/user/<int:id_us>", dislike_comment),
	path("delete/article/<int:id_ar>/user/<int:id_us>", delete_article),
	path("edit/article/<int:id_ar>/user/<int:id_us>", edit_article),
	path("delete/comment/<int:id_com>/article/<int:id_ar>/user/<int:id_us>", delete_comment),
	path("edit/comment/<int:id_com>/article/<int:id_ar>/user/<int:id_us>", edit_comment),
]
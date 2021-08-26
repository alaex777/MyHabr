from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(unique=True, max_length=32, default="")
	email = models.EmailField(unique=True, default="")
	password = models.CharField(max_length=128, default="")
	category = models.CharField(max_length=32, default="")
	description = models.TextField(default="")
	date_registered = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)

class Article(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET("Deleted user"))
	content = models.TextField(default="")
	date_added = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=32, default="")
	name = models.CharField(max_length=128, default="")
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

class Comment(models.Model):
	content = models.CharField(max_length=256, default="")
	time_added = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.SET("Deleted user"))
	article = models.ForeignKey(Article, on_delete=models.SET("Deleted user"))
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

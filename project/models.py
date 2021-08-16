from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(unique=True, max_length=32)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	category = models.CharField(max_length=32)

class Article(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET("Deleted user"))
	content = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=32)
	name = models.CharField(max_length=128)

class Comment(models.Model):
	content = models.CharField(max_length=256)
	time_added = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.SET("Deleted user"))
	article = models.ForeignKey(Article, on_delete=models.SET("Deleted user"))

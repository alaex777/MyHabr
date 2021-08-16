from django import forms
from django.forms import ModelForm
from .models import User, Article 

class Login(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=128)

class Register(ModelForm):
	class Meta:
		model = User
		fields = ("username", "email", "password",)

class CreateArticle(ModelForm):
	class Meta:
		model = Article
		fields = ("name", "category", "content",)
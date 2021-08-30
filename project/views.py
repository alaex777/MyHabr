from django.shortcuts import render, redirect
from django.views import View
from .models import Article, User, Comment, CommentRelationship, ArticleRelationship
from .forms import Login, Register, CreateArticle, CreateComment

# Create your views here.

def start(request, id):
	query = Article.objects.all()
	if len(query) >= 5:
		query = query[-1:-6:-1]
	else:
		query = query[::-1]
	return render(request, "start.html", 
		context={"name": "My Habr", "query": query, "id": id})

def login(request):
	form = Login(request.POST)
	if request.method == "POST":
		if form.is_valid():
			try:
				user = User.objects.get(username=str(form.cleaned_data["username"]))
				if user.password != str(form.cleaned_data["password"]):
					return "Incorrect Password"
				id = str(user.id)
				address = "/user/"+id+"/"
				return redirect(address)
			except:
				print("No such User")
	return render(request, "login.html", context={"form": form})

def register(request):
	form = Register(request.POST)
	if request.method == "POST":
		if form.is_valid():
			user = User(username=str(form.cleaned_data["username"]), 
				email=str(form.cleaned_data["email"]), 
				password=str(form.cleaned_data["password"]), 
				category="Watch only")
			user.save()
			id = str(user.id)
			address = "/user/"+id+"/"
			return redirect(address)
	return render(request, "register.html", context={"form": form})

def user_page(request, id):
	user = User.objects.get(pk=id)
	try:
		articles = Article.objects.filter(author=user)
	except:
		articles = None
	if request.GET.get("Add") == "Add Article":
		address = "create_article/user/" + str(id) + "/"
		return redirect(address)
	return render(request, "user.html", context={"user": user, "articles": articles})

def create_article(request, id):
	form = CreateArticle(request.POST)
	if request.method == "POST":
		if form.is_valid():
			user = User.objects.get(pk=id)
			article = Article(author=user, 
				content=str(form.cleaned_data["content"]), 
				category=str(form.cleaned_data["category"]), 
				name=str(form.cleaned_data["name"]))
			article.save()
			address = "/user/"+id+"/"
			return redirect(address)
	return render(request, "create_article.html", context={"form": form})

def article(request, id, pk):
	article = Article.objects.get(pk=id)
	likes = len(ArticleRelationship.objects.filter(article=article, category="Like"))
	dislikes = len(ArticleRelationship.objects.filter(article=article, category="Dislike"))
	user = User.objects.get(pk=pk)
	article_likes = [i["article"] for i in ArticleRelationship.objects.filter(user=user, category="Like").values("article")]
	article_dislikes = [i["article"] for i in ArticleRelationship.objects.filter(user=user, category="Dislike").values("article")]
	comment_likes = [i["comment"] for i in CommentRelationship.objects.filter(user=user, category="Like").values("comment")]
	comment_dislikes = [i["comment"] for i in CommentRelationship.objects.filter(user=user, category="Dislike").values("comment")]
	form = CreateComment(request.POST)
	try:
		comments = Comment.objects.filter(article=article)
	except:
		comments = None
	if request.method == "POST":
		if form.is_valid():
			comment = Comment(content=str(form.cleaned_data["content"]), author=user, article=article)
			comment.save()
			return redirect("/article/"+str(id)+"/user/"+str(pk))
	return render(request, "article.html", 
		context={"article": article, 
				"comments": comments, 
				"user": user, 
				"form": form, 
				"likes": likes, 
				"dislikes": dislikes, 
				"article_likes": article_likes,
				"article_dislikes": article_dislikes,
				"comment_likes": comment_likes,
				"comment_dislikes": comment_dislikes,})

# create likes and dislikes on comments and articles

def like_article(request, id_ar, id_us):
	article = Article.objects.get(id=id_ar)
	user = User.objects.get(id=id_us)
	author = article.author
	if not ArticleRelationship.objects.filter(user=user, article=article, category="Like"):
		if author != "Deleted user":
			author.rating += 10
			author.save()
		relationship = ArticleRelationship(user=user, article=article, category="Like")
		relationship.save()
	else:
		if author != "Deleted user":
			author.rating -= 10
			author.save()
		relationship = ArticleRelationship.objects.filter(user=user, article=article, category="Like")
		relationship.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)

def dislike_article(request, id_ar, id_us):
	article = Article.objects.get(id=id_ar)
	user = User.objects.get(id=id_us)
	author = article.author
	if not ArticleRelationship.objects.filter(user=user, article=article, category="Dislike"):
		if author != "Deleted user":
			author.rating -= 10
			author.save()
		relationship = ArticleRelationship(user=user, article=article, category="Dislike")
		relationship.save()
	else:
		if author != "Deleted user":
			author.rating += 10
			author.save()
		relationship = ArticleRelationship.objects.filter(user=user, article=article, category="Dislike")
		relationship.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)

def like_comment(request, id_com, id_ar, id_us):
	comment = Comment.objects.get(id=id_com)
	user = User.objects.get(id=id_us)
	author = comment.author
	if not CommentRelationship.objects.filter(user=user, comment=comment, category="Like"):
		if author != "Deleted user":
			author.rating += 3
			author.save()
		relationship = CommentRelationship(user=user, comment=comment, category="Like")
		relationship.save()
	else:
		if author != "Deleted user":
			author.rating -= 3
			author.save()
		relationship = CommentRelationship.objects.filter(user=user, comment=comment, category="Like")
		relationship.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)

def dislike_comment(request, id_com, id_ar, id_us):
	comment = Comment.objects.get(id=id_com)
	user = User.objects.get(id=id_us)
	author = comment.author
	if not CommentRelationship.objects.filter(user=user, comment=comment, category="Dislike"):
		if author != "Deleted user":
			author.rating -= 3
			author.save()
		relationship = CommentRelationship(user=user, comment=comment, category="Dislike")
		relationship.save()
	else:
		if author != "Deleted user":
			author.rating += 3
			author.save()
		relationship = CommentRelationship.objects.filter(user=user, comment=comment, category="Dislike")
		relationship.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)

# edit and delete comments and articles

def edit_comment(request, id_com, id_ar, id_us):
	comment = Comment.objects.get(id=id_com)
	article = Article.objects.get(id=id_ar)
	user = User.objects.get(id=id_us)
	form = CreateComment(request.POST)
	if request.method == "POST":
		if form.is_valid():
			comment.content = str(form.cleaned_data["content"])
			comment.save()
			address = "/article/" + str(id_ar) + "/user/" + str(id_us)
			return redirect(address)
	return render(request, "edit_comment.html", context={"form": form, "comment": comment, "article": article, "user": user})

def delete_comment(request, id_com, id_ar, id_us):
	comment = Comment.objects.get(id=id_com)
	comment.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)

def edit_article(request, id_ar, id_us):
	article = Article.objects.get(id=id_ar)
	user = User.objects.get(id=id_us)
	form = CreateArticle(request.POST)
	if request.method == "POST":
		if form.is_valid():
			article.name = str(form.cleaned_data["name"])
			article.content = str(form.cleaned_data["content"])
			article.category = str(form.cleaned_data["category"])
			article.save()
			address = "/article/" + str(id_ar) + "/user/" + str(id_us)
			return redirect(address)
	return render(request, "edit_article.html", context={"form": form, "article": article, "user": user})

def delete_article(request, id_ar, id_us):
	article = Article.objects.get(id=id_ar)
	article.delete()
	address = "/article/" + str(id_ar) + "/user/" + str(id_us)
	return redirect(address)





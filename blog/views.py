import logging
from django.shortcuts import render, redirect
from django.template import RequestContext
from google.appengine.api import users
from blog.decorators import login_required
from blog.forms import BlogPostForm
from blog.models import BlogPost


def blog_render(request, template, params={}):
	context = RequestContext(request)
	user = users.get_current_user()
	if user:
		#logging.info("user exists: " + user.email())
		params["logout"] = users.create_logout_url("/")
		params["email"] = user.email()
	else:
		#logging.info("user does not exist: ")
		params["login"] = users.create_login_url("/")
	return render(request=request,
	              template_name=template,
	              dictionary=params,
	              context_instance=context)


def home(request):
	blog_posts = BlogPost.query().order(-BlogPost.datetime).fetch()
	params = {"blog_posts": blog_posts}
	return blog_render(request, "home.html", params)


def login(request):
	return redirect(users.create_login_url('/'))


def logout(request):
	return redirect(users.create_logout_url('/'))


@login_required
def post_add(request):
	if request.method == "GET":
		form = BlogPostForm()
		params = {"form": form}
		return blog_render(request, "post_add.html", params)

	elif request.method == "POST":
		form = BlogPostForm(request.POST)

		if form.is_valid():
			BlogPost.create(title=form.cleaned_data["title"],
			                content=form.cleaned_data["content"],
			                author=users.get_current_user().email())
		else:
			params = {"form": form}
			return blog_render(request, "post_add.html", params)

		return redirect("home")


def post_view(request, post_id):
	post = BlogPost.get_by_id(int(post_id))
	params = {"post": post}
	return blog_render(request, "post_view.html", params)


@login_required
def post_edit(request, post_id):
	post = BlogPost.get_by_id(int(post_id))
	user = users.get_current_user()
	if request.method == "GET" and post.author == user.email():
		form = BlogPostForm({"title": post.title, "content": post.content})
		params = {"form": form, "post": post}
		return blog_render(request, "post_edit.html", params)
	elif request.method == "POST" and post.author == user.email():
		form = BlogPostForm(request.POST)

		if form.is_valid():
			BlogPost.edit(post_id=int(post_id),
			              title=form.cleaned_data["title"],
			              content=form.cleaned_data["content"])
		else:
			params = {"form": form}
			return blog_render(request, "post_add.html", params)

		return redirect("home")
	else:
		return redirect("forbidden")


@login_required
def post_delete(request, post_id):
	post = BlogPost.get_by_id(int(post_id))
	user = users.get_current_user()
	if request.method == "POST" and post.author == user.email():
		post.key.delete()
		return redirect("home")
	else:
		return redirect("forbidden")


def forbidden(request):
	return blog_render(request, "403.html")
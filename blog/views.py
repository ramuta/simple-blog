import logging
from django.shortcuts import render, redirect
from django.template import RequestContext
from google.appengine.api import users
from blog.decorators import login_required


def blog_render(request, template, params={}):
	context = RequestContext(request)
	user = users.get_current_user()
	if user:
		logging.info("user exists: " + user.email())
		params["logout"] = users.create_logout_url("/")
		params["email"] = user.email()
	else:
		logging.info("user does not exist: ")
		params["login"] = users.create_login_url("/")
	return render(request=request,
	              template_name=template,
	              dictionary=params,
	              context_instance=context)


def home(request):
	params = {"name": "Matej"}
	return blog_render(request, "home.html", params)


def login(request):
	return redirect(users.create_login_url('/'))


def logout(request):
	return redirect(users.create_logout_url('/'))


@login_required
def post_add(request):
	if request.method == "GET":
		return blog_render(request, "post_add.html")
	elif request.method == "POST":
		title = request.POST.get("title", "None")
		logging.info("naslov: " + title)
		return blog_render(request, "home.html")


def post_view(request):
	pass
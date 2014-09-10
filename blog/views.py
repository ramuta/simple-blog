import logging
from django.shortcuts import render_to_response, render


def home(request):
	params = {"name": "Matej"}
	return render_to_response("home.html", params)


def post_add(request):
	if request.method == "GET":
		return render(request, "post_add.html")
	elif request.method == "POST":
		title = request.POST.get("title", "None")
		logging.info("naslov: " + title)
		return render(request, "home.html")


def post_view(request):
	pass
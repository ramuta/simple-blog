from django.shortcuts import render_to_response


def home(request):
	params = {"name": "Matej"}
	return render_to_response("home.html", params)


def post_add(request):
	pass


def post_view(request):
	pass
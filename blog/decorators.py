import logging
from django.shortcuts import redirect
from google.appengine.api import users
from blog.models import BlogPost


def login_required(view):
    def check_login(request, *args, **kw):
        user = users.get_current_user()
        if user:
            return view(request, *args, **kw)
        else:
            return redirect(users.create_login_url("/"))
    return check_login
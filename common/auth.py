from django.http import HttpResponseRedirect
from google.appengine.api import users
from blog.models import Post
import settings

def login_required(func):
    def _wrapper(request, *args, **kwargs):
        user = users.get_current_user()
        if user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
    return _wrapper

def author_required(func):
    def _wrapper(request, *args, **kwargs):
        if is_author():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
    return _wrapper

def post_author_required(pos=1):
    def _decorate(func):
        def _wrapper(request, *args, **kwargs):
            post_id = kwargs['post_id']            
            if is_post_author(post_id):
                return func(request, *args, **kwargs)    
            else:
                return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
        return _wrapper
    return _decorate

def admin_required(func):
    def _wrapper(request, *args, **kwargs):
        if is_admin():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
    return _wrapper

def is_author():
    user = users.get_current_user()
    if user:
        return settings.AUTHORS.count(user.email()) > 0
    return False

def is_post_author(post_id):
    user = users.get_current_user()
    if user:
        is_author = (settings.AUTHORS.count(user.email()) > 0)
        if is_author:
            post = Post.get_by_id(int(post_id))
            if post:
                return post.author.email() == user.email()
            return False
        return False
    return False

def is_admin():
    user = users.get_current_user()
    if user:
        return settings.ADMINS.count(user.email()) > 0

    return False

from django.http import HttpResponseRedirect
from google.appengine.api import users
import settings

def login_required(func):
    def _wrapper(request, *args, **kw):
        user = users.get_current_user()
        if user:
            return func(request, *args, **kw)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))

    return _wrapper

def admin_required(func):
    def _wrapper(request, *args, **kw):
        if is_admin():
            return func(request, *args, **kw)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))

    return _wrapper

def is_admin():
    user = users.get_current_user()
    if user:
        return settings.AUTHORS.count(user.email()) > 0

    return False


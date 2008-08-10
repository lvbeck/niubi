from django.http import HttpResponseRedirect
from google.appengine.api import users


def login(request):
    if request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = '/'
    return HttpResponseRedirect(users.create_login_url(next))

def logout(request):
    return HttpResponseRedirect(users.create_logout_url('/'));
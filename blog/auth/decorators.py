from django.http import HttpResponseRedirect
from google.appengine.api import users
from blog.models import *

def post_edit_auth_required(pos=1):
    def _decorate(func):
        def _wrapper(request, *args, **kwargs):
            if request.user.has_perm('post_edit'):                
                post_id = kwargs['post_id']
                post = Post.get_by_id(int(post_id))
                if request.user.email() == post.author.email(): 
                    return func(request, *args, **kwargs)
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
        return _wrapper
    return _decorate
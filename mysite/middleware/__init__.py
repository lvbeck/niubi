from mysite.blog.models import Category, Post

class InfoMiddleware(object):
  def process_request(self, request):
      if not hasattr(request, 'categories'):
          request.categories = Category.all().order('-post_count')      
      if not hasattr(request, 'most_read_posts'):
          request.most_read_posts = Post.all().order('-read_count')[:10]   
      return None
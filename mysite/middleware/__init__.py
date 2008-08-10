from mysite.blog.models import Category

class InfoMiddleware(object):
  def process_request(self, request):
      if not hasattr(request, 'categories'):
          request.categories = Category.all().order('-post_count')
    
      return None
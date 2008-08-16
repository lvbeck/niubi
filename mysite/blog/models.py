# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.ext import search
# from mysite.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty()
    post_count = db.IntegerProperty(default=0)
    #logo = db.StringProperty()
    
    def __str__(self):
        return self.name

class Post(search.SearchableModel):
    author = db.UserProperty()
    title = db.TextProperty(required=True, verbose_name=u'标题')
    # tag = db.StringProperty(verbose_name=u'标签')
    # tags = db.StringListProperty(verbose_name=u'标签')
    tags = db.ListProperty(item_type=db.Category, verbose_name=u'标签') # redudant way
    # tags = db.ReferenceListProperty(verbose_name=u'标签') # do not use many-to-many

    content = db.TextProperty(required=True, verbose_name=u'内容')
    create_time = db.DateTimeProperty(auto_now_add=True)
    update_time = db.DateTimeProperty(auto_now=True)
    category = db.ReferenceProperty(Category, required=True, verbose_name=u'类别')
    is_published = db.BooleanProperty(verbose_name=u'已发布')
    comment_count = db.IntegerProperty(default=0)
    read_count = db.IntegerProperty(default=0)
    
    def getComments(self):
        c = {}
        f = 1
        for comment in Comment.all().filter('post', self).order('create_time'):
            comment.floor = f
            if comment.parent_comment is not None:
                comment.parent_comment_floor = c[comment.parent_comment.key().id()].floor
            c[comment.key().id()] = comment
            f += 1
        self.comments = sorted(c.values(),cmp=lambda x,y: cmp(x.key().id(), y.key().id()))
            
    def getTags(self, str):
        self.tags = []    
        twords = str.split(' ')        
        if twords is not None: 
            for word in twords:
                tag = db.Category(word)
                self.tags.append(tag)
                
    def get_absolute_url(self) :
        return '/post/%s/'%self.key().id()
    
    # redundant data since GAE do not support m:n relations     
    def putTags(self, str, oTags):
        twords = str.split(' ')        
        if twords is not None:
            for word in twords:
                tag = Tag.get_or_insert(word)
                tag.name = word
                tag.getPosts()
                tag.countPosts()
                tag.put()
        if oTags is not None:       
            for oTag in oTags:
                tag = Tag.get_by_key_name(oTag)
                tag.countPosts()
                tag.put() # update old tags post count
                if tag.post_count == 0:
                    tag.delete()    
    
class Comment(db.Model):
    author = db.UserProperty()
    post = db.ReferenceProperty(Post)
    parent_comment = db.SelfReferenceProperty()
    content = db.StringProperty(multiline=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
  
class Tag(db.Model):
    name = db.StringProperty()
    post_count = db.IntegerProperty(default=1)
    
    def countPosts(self):
        self.post_count = 0
        posts = Post.all() # Datastore  do not support 'in' filter in query
        if posts is not None:
            for post in posts:
                if post.tags is not None:
                    for tag in post.tags:
                        if tag == self.name:
                            self.post_count += 1
    def getPosts(self):
        self.posts = []
        posts = Post.all() # Datastore  do not support 'in' filter in query
        if posts is not None:
            for post in posts:
                if post.tags is not None:
                    for tag in post.tags:
                        if tag == self.name:
                            self.posts.append(post)
        
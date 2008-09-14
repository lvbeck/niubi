# -*- coding: utf-8 -*-
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import search

class Category(db.Model):
    name = db.StringProperty()
    post_count = db.IntegerProperty(default=0)
    #logo = db.StringProperty()
    
    def __str__(self):
        return self.name

class Post(search.SearchableModel):
    author = db.UserProperty()
    title = db.TextProperty(required=True, verbose_name=u'标题')
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
    
    def getTags(self, min_relevance=0.00):                        
        return [entry.tag for entry in PostTag.all().filter('post =',self).filter('relevance > ',min_relevance).order('-relevance').order('-create_time')]

    def get_absolute_url(self) :
        return '/post/%s/'%self.key().id()
    
    def deleteTags(self):
        for relation in PostTag.all().filter('post =',self):
            relation.delete()
        Tag.clean()
               
    def putTags(self, str):
        self.deleteTags()
        twords = str.split(' ')        
        if twords is not None:
            for word in twords:
                tag = Tag.get_or_insert(word)                                
                tag.name = word
                tag.put()
                relation = PostTag(post=self,tag=tag)
                relation.put()
                tag.post_count = tag.countPosts()
                tag.put()
    
    @staticmethod
    def getNextMonth(d):
        return datetime(d.year + 1, 1, 1) if d.month == 12 else datetime(d.year, d.month + 1, 1)
    
    @staticmethod
    def getByYM(year, month):
        begin = datetime.strptime(year+'-'+month+'-01','%Y-%m-%d')
        end = Post.getNextMonth(begin)
        return Post.all().filter('is_published', True).filter('create_time >= ', begin).filter('create_time <= ', end)    
        
    @staticmethod
    def getArchives():
        l = []
        archive = Post.all().order('create_time').get().create_time       
        while archive < datetime.today():
            archive = Post.getNextMonth(archive)
            l.append(archive)
        l.reverse()
        return l
        
    
class Comment(db.Model):
    author = db.UserProperty()
    post = db.ReferenceProperty(Post)
    parent_comment = db.SelfReferenceProperty()
    content = db.StringProperty(multiline=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
  
class Tag(db.Model):
    name = db.StringProperty()     
    post_count = db.IntegerProperty(default=0)
    
    def countPosts(self):
        return PostTag.all().filter('tag =', self).count()
    
    def hasPost(self):
        return True if PostTag.all().filter('tag =', self).get() else False    
        
    def getRelation(self, post):
        return PostTag.all().filter('tag =', self).filter('post =', post).get()
    
    def getPosts(self, min_relevance=0.00):                 
        return [entry.post for entry in PostTag.all().filter('tag =',self).filter('relevance > ',min_relevance).order('-relevance').order('-create_time')]         
    
    @staticmethod
    def clean():
        for tag in Tag.all():
            if tag.hasPost() is not True:
                tag.delete()
                
class PostTag(db.Model):
    post = db.ReferenceProperty(Post, required=True, collection_name='tags', verbose_name=u'标签')
    tag = db.ReferenceProperty(Tag, required=True, collection_name='posts', verbose_name=u'文章')
    create_time = db.DateTimeProperty(auto_now_add=True)
    relevance = db.FloatProperty(default=1.00)
    
    @staticmethod
    def getTags(post, min_relevance=0.00):
        if not post: return []                 
        return [entry.tag for entry in PostTag.all().filter('post =',post).filter('relevance > ',min_relevance).order('-relevance').order('-create_time')]
    
    @staticmethod
    def getPosts(tag, min_relevance=0.00):
        if not tag: return []       
        return [entry.post for entry in PostTag.all().filter('tag =',tag).filter('relevance > ',min_relevance).order('-relevance').order('-create_time')]    
    
  
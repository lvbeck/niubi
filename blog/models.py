# -*- coding: utf-8 -*-
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import search

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()
    parent_category = db.SelfReferenceProperty()    
    post_count = db.IntegerProperty(default=0)
    #logo = db.StringProperty()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self) :
        return '/category/%s/'%self.key().id()
    
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
    
    def getTagsString(self, separator=' ', min_relevance=0.00):
        return separator.join(map(lambda x:x.name, self.getTags(min_relevance)))
    
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
        Tag.generateCloud()
    
    @staticmethod
    def getNextMonth(d):
        return datetime(d.year + 1, 1, 1) if d.month == 12 else datetime(d.year, d.month + 1, 1)
    
    @staticmethod
    def getByYM(year, month):
        begin = datetime.strptime(year+'-'+month+'-01','%Y-%m-%d')
        end = Post.getNextMonth(begin)
        return Post.all().filter('is_published', True).filter('create_time >= ', begin).filter('create_time <= ', end).order('-create_time')    
        
    @staticmethod
    def getArchives():
        l = []
        if Post.all().get():
            archive = Post.all().order('create_time').get().create_time       
            while archive < datetime.today():            
                l.append(archive)
                archive = Post.getNextMonth(archive)
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
    font_size = db.IntegerProperty(default=0)

    def __str__(self):
        return self.name
       
    def countPosts(self):
        return PostTag.all().filter('tag =', self).count()
    
    def hasPost(self):
        return True if PostTag.all().filter('tag =', self).get() else False    
        
    def getRelation(self, post):
        return PostTag.all().filter('tag =', self).filter('post =', post).get()
    
    def getPosts(self, min_relevance=0.00):                 
        return [entry.post for entry in PostTag.all().filter('tag =',self).filter('relevance > ',min_relevance).order('-relevance').order('-create_time')]         

    def get_absolute_url(self):
        return '/tag/%s/'%self.name
    
    def __cmp__(self, other):
        return cmp(self.post_count, other.post_count)  
    
    @staticmethod
    def generateCloud():
        tag_list = Tag.all().order('-post_count')
        nbr_of_buckets = 8
        base_font_size = 11
        tresholds = []
        max_tag = max(tag_list)
        min_tag = min(tag_list)
        delta = (float(max_tag.post_count) - float(min_tag.post_count)) / (float(nbr_of_buckets))
        # set a treshold for all buckets
        for i in range(nbr_of_buckets):
            tresh_value =  float(min_tag.post_count) + (i+1) * delta
            tresholds.append(tresh_value)
        # set font size for tags (per bucket)
        for tag in tag_list:
            font_set_flag = False
            for bucket in range(nbr_of_buckets):
                if font_set_flag == False:
                    if (tag.post_count <= tresholds[bucket]):
                        tag.font_size = base_font_size + bucket * 2
                        tag.save()
                        font_set_flag = True
        
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
        

    
  
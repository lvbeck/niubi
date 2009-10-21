# -*- coding: utf-8 -*-
import logging
import settings
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.api import mail
from http import object_list
from http.auth import *
from shared.models import RequestLogger
from models import Post, Comment, Category, Tag
from forms import PostForm, CommentForm

@author_required
def add_post(request):
    if request.method == 'GET':
        form = PostForm() 
    if request.method == 'POST':
        form = PostForm(request.POST)
        logging.getLogger().debug(form)
        if form.is_valid():
            post = form.save()
            post.author = users.get_current_user()                
            post.putTags(request.POST['tagsString'])
            post.put()
            post.category.post_count += 1
            post.category.put()                 
            return HttpResponseRedirect('/')
    return render_to_response('operate_post.html', {'form': form}, context_instance=RequestContext(request))  

@admin_required
def list_all_post(request):
    posts = Post.all().order('-create_time');
    return object_list(request, queryset=posts, allow_empty=True,
            template_name='list_post.html', extra_context={'is_admin': is_admin()},
            paginate_by=settings.POST_LIST_PAGE_SIZE)      
    
def list_post(request):
    posts = Post.all().order('-create_time')
    if (not is_admin()):
        posts = posts.filter("is_published", True)  
    return object_list(request, queryset=posts, allow_empty=True,
            template_name='list_post.html', extra_context={'is_author': is_author()},
            paginate_by=settings.POST_LIST_PAGE_SIZE)  
    
@author_required
def add_category(request):
    if request.method == 'POST':
        category = Category()
        category.name = request.POST['name']
        category.slug = request.POST['slug']
        category.put();   
        return HttpResponseRedirect('/category/add')  
    return render_to_response('add_category.html', context_instance=RequestContext(request))

@post_author_required()
def edit_post(request, post_id):
    post = Post.get_by_id(int(post_id))
    if not post:
        raise Http404   
    if request.method == 'GET':
        form = PostForm({'title': post.title, 
                         'content': post.content, 
                         # 'tags': post.tags, 
                         'category': post.category.key(), 
                         'is_published': post.is_published})
        tagsString = post.getTagsString()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            modified_post = form.save(commit=False)
            if modified_post.category.key() != post.category.key():
                post.category.post_count -= 1
                post.category.put()
                modified_post.category.post_count += 1
                modified_post.category.put()
            post.title = modified_post.title
            post.category = modified_post.category                    
            post.content = modified_post.content
            post.is_published = modified_post.is_published
            post.putTags(request.POST['tagsString'])
            post.put()
            return HttpResponseRedirect('/post/%s/'%post.key().id())  
    return render_to_response('operate_post.html', {'form': form, 'id':post.key().id, 'tagsString': tagsString}, context_instance=RequestContext(request))

def print_post (request, post_id):
    post = Post.get_by_id(int(post_id))
    post.getComments()    	
    if not post:
        raise Http404    
    if not is_admin() and not post.is_published:
        raise Http404
    return render_to_response('print_post.html', {'post':post}, context_instance=RequestContext(request))

def view_post(request, post_id):
    post = Post.get_by_id(int(post_id))
    if not post:
        raise Http404    
    if not is_admin() and not post.is_published:
        raise Http404  
    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST['comment']
        comment.author = users.get_current_user()
        comment.post = post
        if request.POST['parent_comment'] != "":
            parent_comment = Comment.get_by_id(int(request.POST['parent_comment']))
            comment.parent_comment = parent_comment
        comment.put()      
        post.comment_count = post.comment_count + 1
        post.put()        
        mail.send_mail(sender="no-reply@niubi.de",
                       to=post.author.email(),
                       subject=(u'牛逼 - 你的文章%s有了新评论'%post.title).encode('utf8'),
                       body=(u'''%s在你的文章%s上留了评论: 

%s
 
点击这个链接回复: http://www.niubi.de/post/%s/''' %(comment.author.nickname(), post.title, comment.content, post.key().id())).encode('utf8')
                       )     
        comments = Comment.all().filter('post', post)
        sent_users = []
        for c in comments:
            if not contains_user(sent_users, c.author):
                mail.send_mail(sender="no-reply@niubi.de",
                               to=c.author.email(),
                               subject=(u'牛逼 - 你参与评论的文章%s有了新评论'%post.title).encode('utf8'),
                               body=(u'''%s在文章%s上留了评论: 

%s
 
点击这个链接回复: http://www.niubi.de/post/%s/''' %(comment.author.nickname(), post.title, comment.content, post.key().id())).encode('utf8')
                       )
                sent_users.append(c.author)
        
        return HttpResponseRedirect('/post/%s' % post.key().id())
    
    post.read_count = post.read_count + 1
    post.put()
    post.getComments()       
    return render_to_response('view_post.html', 
                              {'post':post,'is_post_author':is_post_author(post_id)}, context_instance=RequestContext(request))
    
def contains_user(users, user):
    for u in users:
        if u.email() == user.email():
            return True
    return False

def update(request):
    pass
#    posts = Post.all().order('-create_time')
#    for post in posts:
#        delattr(post, "tags")
#        post.put()
#        if not post.category.post_count:
#            post.category.post_count = 1
#        else:
#            post.category.post_count = post.category.post_count + 1
#        post.category.put()       
    return HttpResponse('OK')

def about(request):
    str = (u'<br/><p>&nbsp;&nbsp;此站点基于学习及娱乐目的, 联系方式：admin 在 niubi.de, 无事勿扰, 谢谢合作</p>').encode('utf8')
    return HttpResponse(str, content_type='text/plain')
    #return render_to_response('about.html', context_instance=RequestContext(request))

def download(request):
    str = (u'<br/><p>&nbsp;&nbsp;项目源代码：<a href="http://code.google.com/p/niubi/" target="_blank">http://code.google.com/p/niubi</a></p>').encode('utf8')
    return HttpResponse(str, content_type='text/plain')
    #return render_to_response('download.html', context_instance=RequestContext(request))

def list_category_post(request, category_id):
    category = Category.get_by_id(int(category_id))
    if not category:
        raise Http404  
    posts = Post.all().filter('category', category).order('-create_time')

    return object_list(request, queryset=posts, allow_empty=True,
            template_name='list_category_post.html', extra_context={'is_author': is_author(), 'category': category},
            paginate_by=settings.POST_LIST_PAGE_SIZE) 

def list_tag_post(request,tag_name):
    tag = Tag.get_by_key_name(tag_name)
    if not tag:
        raise Http404  
    # tag.getPosts().order('-create_time')
    tag.post_list = tag.getPosts()
    return object_list(request, queryset=tag.post_list, allow_empty=True,
            template_name='list_tag_post.html', extra_context={'is_author': is_author(), 'is_author': is_author(), 'tag': tag},
            paginate_by=settings.POST_LIST_PAGE_SIZE)     
    
def search(request):
    if request.REQUEST.has_key('q'):
        keywords = request.GET['q']
        logging.getLogger().info(keywords)
        posts = Post.all().search(keywords).order('-create_time')
        return object_list(request, queryset=posts, allow_empty=True,
                template_name='search_post.html', extra_context={'keywords': keywords},
                paginate_by=settings.POST_LIST_PAGE_SIZE)
    else:
        return HttpResponseRedirect('/')
    
def sitemap(request):
    str = '''<?xml version="1.0" encoding="UTF-8"?>
            <?xml-stylesheet type="text/xsl" href="/static/xsl/sitemap.xsl"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
               <url>
                  <loc>http://www.niubi.de/</loc>
                  <changefreq>weekly</changefreq>
                  <priority>0.9</priority>
               </url>
        '''      
    posts = Post.all().filter('is_published', True)
    for post in posts:
        str += '''<url>
                      <loc>http://www.niubi.de/post/%s/</loc>
                      <changefreq>weekly</changefreq>
                      <priority>0.8</priority>
                   </url>
                '''%post.key().id()
                
    categories = Category.all().order('-post_count')
    for category in categories:
        str += '''<url>
                      <loc>http://www.niubi.de/category/%s/</loc>
                      <changefreq>monthly</changefreq>
                      <priority>0.8</priority>
                   </url>
                '''%category.key().id()
    tags = Tag.all().order('-post_count')
    for tag in tags:
        str += '''<url>
                      <loc>http://www.niubi.de/tag/%s/</loc>
                      <changefreq>weekly</changefreq>
                      <priority>0.8</priority>
                   </url>
                '''%tag.name
    str +=      '''<url>
                  <loc>http://www.niubi.de/about/</loc>
                  <changefreq>yearly</changefreq>
                  <priority>0.8</priority>
               </url>'''            
    str += '</urlset>'
    return HttpResponse(str, content_type='text/xml')

def archives(request, year, month):
    #if month is not int:
        #raise Http404
    #return HttpResponse(month, content_type='text/plain')
    posts = Post.getByYM(year, month)
    return object_list(request, queryset=posts, allow_empty=True,
            template_name='list_archives_post.html', extra_context={'is_author': is_author(), 'year': year, 'month': month},
            paginate_by=settings.POST_LIST_PAGE_SIZE)    

@admin_required
def view_log(request):
    if request.method == 'GET':
        str = '<html><body><h1>Logger</h1>'
        for log in RequestLogger.all().order('-create_time').fetch(5,0):
            str += '<p>date: %s</p>' % log.create_time
            str += '<h1>Request</h1>'
            str += '<pre>%s</pre>' % cgi.escape(log.request)
            str += '<h1>Reponse</h1>'
            str += '<pre>%s</pre>' % cgi.escape(log.response)
            str += '<hr />'
        str += '</body></html>'          
    return HttpResponse(str)

@admin_required      
def delete_log(request):
    for log in RequestLogger.all():
        log.delete()
    return HttpResponseRedirect('/rpc/view_log/')    
    
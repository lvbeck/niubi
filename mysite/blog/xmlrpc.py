# -*- coding: utf-8 -*-
import wsgiref.handlers
import xmlrpclib
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from mysite.utils.rpc import PlogXMLRPCDispatcher
from mysite.utils.rpc.auth import login_required as rpc_login_required
from mysite.utils.http.auth import admin_required as http_admin_required
from mysite.blog.models import *

def format_date(d):
    if not d: return None
    return xmlrpclib.DateTime(d.isoformat())
    
def entry_struct(entry):
    categories=[]
    if entry.categorie_keys:
        categories =[cate.name for cate in entry.categories]
        
    struct = {
        'postid': entry.key().id(),
        'title': entry.title,
        'link': entry.get_absolute_url(),
        'permaLink': entry.get_absolute_url(),
        'description': unicode(entry.content),
        #'categories': categories,
        'userid': 1,
        'mt_keywords':entry.getTagsString(','),
        'wp_slug':entry.slug,
        'wp_page_order':entry.menu_order,
        # 'mt_excerpt': '',
        # 'mt_text_more': '',
        # 'mt_allow_comments': 1,
        # 'mt_allow_pings': 1}
        }
    if entry.create_time:
        struct['dateCreated'] = format_date(entry.create_time)
    return struct

#-------------------------------------------------------------------------------
#  Test XMLRPC API by saying, "Hello!" to client.
#-------------------------------------------------------------------------------
def demo_sayHello():
    return 'Hello!'

#-------------------------------------------------------------------------------
# metaWeblog
#-------------------------------------------------------------------------------
def _mw_newPost(blogid, struct, publish):
    postid = post.key().id()
    return str(postid)
    
@rpc_login_required()
def metaWeblog_newPost(blogid, struct, publish):
    # Let _mw_newPost do all of the heavy lifting.
    return _mw_newPost(blogid,struct,publish)
    
#-------------------------------------------------------------------------------
#  WordPress API
#-------------------------------------------------------------------------------

@rpc_login_required()
def wp_newCategory(blogid,struct):
    name=struct['name']
    categories = Category.all().filter('name =',name).fetch(1)
    categoryid = ''
    if categories and len(categories):
        categoryid = categories[0].key().id()
    else:
        category = Category()
        category.name = name
        category.slug = urlencode(name)
        category.put();
        categoryid = category.key().id()    
    return str(categoryid)

@rpc_login_required()
def wp_newPage(blogid,struct,publish): 
    struct['post_type'] = 'page'
    # Let _mw_newPost do all of the heavy lifting.    
    return(_mw_newPost(blogid,struct,publish))
        
dispatcher = PlogXMLRPCDispatcher({
    'demo.sayHello':demo_sayHello,    
    #'blogger.getUsersBlogs' : blogger_getUsersBlogs,
    #'blogger.deletePost' : blogger_deletePost,

    #'metaWeblog.newPost' : metaWeblog_newPost,
    #'metaWeblog.editPost' : metaWeblog_editPost,
    #'metaWeblog.getCategories' : metaWeblog_getCategories,
    #'metaWeblog.getPost' : metaWeblog_getPost,
    #'metaWeblog.getRecentPosts' : metaWeblog_getRecentPosts,
    #'metaWeblog.newMediaObject':metaWeblog_newMediaObject,

    #'wp.getCategories':metaWeblog_getCategories,
    'wp.newCategory':wp_newCategory,
    #'wp.newPage':wp_newPage,
    #'wp.getPage':wp_getPage,
    #'wp.getPages':wp_getPages,
    #'wp.editPage':wp_editPage,
    #'wp.getPageList':wp_getPageList,
    #'wp.deletePage':wp_deletePage,
    #'wp.getAuthors':wp_getAuthors,
    #'mt.setPostCategories':mt_setPostCategories
})

# {{{ Handlers
class CallApi(webapp.RequestHandler):
    def get(self):
        Logger(request = self.request.uri, response = '----------------------------------').put()
        self.response.out.write('<h1>please use POST</h1>')

    def post(self):
        #self.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
        request = self.request.body
        response = dispatcher._marshaled_dispatch(request)
        Logger(request = unicode(request, 'utf-8'), response = unicode(response, 'utf-8')).put()
        self.response.out.write(response)

class View(webapp.RequestHandler):
    @http_admin_required
    def get(self):
    	self.write('<html><body><h1>Logger</h1>')
    	for log in Logger.all().order('-date').fetch(5,0):
    	    self.write("<p>date: %s</p>" % log.date)
    	    self.write("<h1>Request</h1>")
    	    self.write('<pre>%s</pre>' % cgi.escape(log.request))
    	    self.write("<h1>Reponse</h1>")
    	    self.write('<pre>%s</pre>' % cgi.escape(log.response))
    	    self.write("<hr />")
    	self.write('</body></html>')

class DeleteLog(webapp.RequestHandler):
    @http_admin_required    
    def get(self):
        for log in Logger.all():
            log.delete()
        self.redirect('/rpc/view')
#}}}

def main():
    #webapp.template.register_template_library("filter")
    application = webapp.WSGIApplication(
        [
            ('/rpc', CallApi),
            ('/rpc/view', View),
            ('/rpc/dellog', DeleteLog),
        ],
        debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
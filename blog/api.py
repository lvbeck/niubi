# -*- coding: utf-8 -*-
import xmlrpclib
from lib.xmlrpc.auth import login_required, author_required
from models import *

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
def sayHello():
    return 'Hello!'

#-------------------------------------------------------------------------------
# metaWeblog
#-------------------------------------------------------------------------------
def _mw_newPost(blogid, struct, publish):
    postid = post.key().id()
    return str(postid)
    
@author_required()
def metaWeblog_newPost(blogid, struct, publish):
    # Let _mw_newPost do all of the heavy lifting.
    return _mw_newPost(blogid,struct,publish)
    
#-------------------------------------------------------------------------------
#  WordPress API
#-------------------------------------------------------------------------------

@author_required()
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

@author_required()
def wp_newPage(blogid,struct,publish): 
    struct['post_type'] = 'page'
    # Let _mw_newPost do all of the heavy lifting.    
    return(_mw_newPost(blogid,struct,publish))



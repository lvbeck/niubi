# -*- coding: utf-8 -*-
import os,logging
from google.appengine.ext import db
    
class RequestLogger(db.Model):
    request = db.TextProperty()
    response = db.TextProperty()
    create_time = db.DateTimeProperty(auto_now_add=True)
'''
class Site(db.Model):
    domain = db.StringProperty(required=True, verbose_name=u'domain name')
    name = db.StringProperty(required=True, verbose_name=u'display name')
    
mysite=None
def InitSiteData():
    import settings
    global mysite
    mysite = Site(key_name = 'default', domain=os.environ['HTTP_HOST'], name=settings.SITE_NAME)
    mysite.save()
    
def site_init():
    logging.info('module setting reloaded')
    global mysite
    mysite = Site.get_by_key_name('default')
    if not mysite:
        mysite=InitSiteData()

site_init()
'''
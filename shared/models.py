# -*- coding: utf-8 -*-
from google.appengine.ext import db

class RequestLogger(db.Model):
    request = db.TextProperty()
    response = db.TextProperty()
    create_time = db.DateTimeProperty(auto_now_add=True)
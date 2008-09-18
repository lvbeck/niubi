# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db

class UserSettings(db.Model):
    user = db.UserProperty()
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    gender = db.StringProperty(choices=("M","F",)) 
    profile = db.TextProperty(verbose_name=u'档案')
    language = db.IntegerProperty()
    im = db.IMProperty()
    birthdate = db.DateProperty()
    website = db.LinkProperty()
    home_phone = db.PhoneNumberProperty()
    work_phone = db.PhoneNumberProperty()
    mobile = db.PhoneNumberProperty()
    fax = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
    
    @staticmethod
    def getByUser(user):
        settings = UserSettings.all().filter('user =',user).get()
        if settings is None:
            settings = UserSettings(user=user)
            settings.put()
        return settings
        # q = db.GqlQuery("SELECT * FROM UserSettings WHERE user = :1", user)
        # return q.get()

    @staticmethod
    def getByCurrentUser():
        user = users.get_current_user()
        return UserSettings.getByUser(user)
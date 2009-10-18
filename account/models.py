# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db

class UserSettings(db.Model):
    user = db.UserProperty()
    lastname = db.StringProperty(verbose_name=u'姓')
    firstname = db.StringProperty(verbose_name=u'名')    
    gender = db.StringProperty(choices=("M","F",), verbose_name=u'性别') 
    profile = db.TextProperty(verbose_name=u'档案')
    language = db.IntegerProperty(verbose_name=u'语言')
    im = db.IMProperty()
    birthdate = db.DateProperty(verbose_name=u'生日')
    website = db.LinkProperty(verbose_name=u'网址')
    home_phone = db.PhoneNumberProperty(verbose_name=u'私人电话')
    work_phone = db.PhoneNumberProperty(verbose_name=u'工作电话')
    mobile = db.PhoneNumberProperty(verbose_name=u'手机')
    fax = db.PhoneNumberProperty(verbose_name=u'传真')
    address = db.PostalAddressProperty(verbose_name=u'地址')
    
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
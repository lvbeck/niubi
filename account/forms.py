# -*- coding: utf-8 -*-
from google.appengine.ext.db import djangoforms as forms
from models import UserSettings

class UserSettingsForm(forms.ModelForm):
    #profile = newforms.CharField(label=u'标题', widget = newforms.TextInput)
    class Meta:
        model = UserSettings
        exclude = ['user','im']


# -*- coding: utf-8 -*-
from google.appengine.ext.db import djangoforms as forms
from models import Post, Comment
from django import newforms

class PostForm(forms.ModelForm):
    title = newforms.CharField(label=u'标题', widget = newforms.TextInput)
    class Meta:
        model = Post
        exclude = ['author', 'comment_count', 'read_count', 'tags']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author']
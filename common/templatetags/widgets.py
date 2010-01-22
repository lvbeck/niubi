# -*- coding: utf8 -*-
from django.template import Library
from blog.models import Post, Category, Tag
from account.models import UserSettings

register = Library()

# use for sidebar widgets
@register.inclusion_tag('widgets.html', takes_context=True)
def widgets(context):
    context['categories'] = Category.all()
    context['tags'] = Tag.all()
    context['archives'] = Post.getArchives()
    context['settings'] = UserSettings.getByCurrentUser()
    return context

"""
def show_widgets(parser, token):
    # {% widgets %}
    return Widgets()

class Widgets(template.Node):
    def render(self, context):
        context['categories'] = Category.all().order('-post_count')
        context['tags'] = Tag.all()
        context['archives'] = Post.getArchives()
        return ''
    
register.tag('widgets', show_widgets)
"""
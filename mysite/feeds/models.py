# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from mysite.blog.models import Post

class LatestEntries(Feed):
    title = u'牛逼最新文章'
    link = '/feeds/latest/'
    description = u'牛逼最新文章'

    def items(self):
        return Post.all().filter("is_published", True).order('-create_time')[: 10]

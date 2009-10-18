# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from feeds.models import LatestEntries
from feeds.models import HottestEntries

feeds = {
    'latest': LatestEntries,
    'hottest': HottestEntries,
}

urlpatterns = patterns('',
    (r'^$', 'blog.views.list_post'),
    (r'update/$', 'blog.views.update'),
    (r'^about/$', 'blog.views.about'),
    (r'^download/$', 'blog.views.download'),
    
    (r'^account/setting/$', 'account.views.setting'),
    
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^rss/latest/$', 'feeds.views.latest_feed_proxy'),
    (r'^rss/hottest/$', 'feeds.views.hottest_feed_proxy'),    
)

urlpatterns += patterns('account.views',    
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
)

urlpatterns += patterns('blog.views',
    (r'^post/add/$', 'add_post'),
    (r'^post/list/$', 'list_post'),
    (r'^post/list_all/$', 'list_all_post'),
    (r'^post/(?P<post_id>\d+)/$', 'view_post'),
    (r'^post/(?P<post_id>\d+)/edit/$', 'edit_post'),
    (r'^post/(?P<post_id>\d+)/print/$', 'print_post'),  
    (r'^archives/(?P<year>\d+)/(?P<month>\d+)/$', 'archives'), 
    (r'^category/add/$', 'add_category'),
    (r'^category/(?P<category_id>\d+)/$', 'list_category_post'),
    (r'^tag/(?P<tag_name>\w+)/$', 'list_tag_post'),
    (r'^search/$', 'search'),  
    (r'^sitemap/$', 'sitemap'),
    (r'^log/view/$', 'view_log'),
    (r'^log/delete/$', 'delete_log'),    
)

urlpatterns += patterns('django_xmlrpc.views',
    (r'^xmlrpc/$', 'handle_xmlrpc'),
)
urlpatterns += patterns('',
    (r'', include('openidgae.urls')),
)

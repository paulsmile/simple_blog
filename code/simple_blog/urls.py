#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import index_page, index_page_2, show_blog, RSSFeed, ProcessTag
from django.conf import settings

admin.autodiscover()
process_tag = ProcessTag()
show_tag_page = process_tag.show

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^index/$', index_page, name='index_page'),
    url(r'^$', index_page_2),
    url(r'^blog/(?P<id>\d+)/$', show_blog, name='detail_blog'),
    url(r'^latest/feed/$', RSSFeed(), name='RSS_url'),
    url(r'^tag_page/(?P<tag_name>.+)/$', show_tag_page, name='tag_page'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )

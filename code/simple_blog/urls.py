#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import index_page, index_page_2, blog_show, RSSFeed
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^index/$', index_page, name='index_page'),
    url(r'^$', index_page_2),
    url(r'^blog/(?P<id>\d+)/$', blog_show, name='detail_blog'),
    url(r'^latest/feed/$', RSSFeed(), name='RSS_url'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )

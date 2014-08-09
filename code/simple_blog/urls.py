#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import RSSFeed, IndexView, IndexRedirectView, ShowBlogView, ShowTagView
from weixin.views import weixin_api
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/$', IndexView.as_view(), name='index_page'),
    url(r'^$', IndexRedirectView.as_view(), name='index_redirect'),
    url(r'^blog/(?P<id>\d+)/$', ShowBlogView.as_view(), name='detail_blog'),
    url(r'^tag_page/(?P<tag_name>.+)/$', ShowTagView.as_view(), name='tag_page'),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^latest/feed/$', RSSFeed(), name='RSS_url'),

    url(r'^weixin/$', weixin_api, name='weixin_api'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )

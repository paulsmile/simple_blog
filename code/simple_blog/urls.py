#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from blog.views import (RSSFeed, IndexView, IndexRedirectView, ShowBlogView,
                        ShowTagView, HandleCommentAsync, GetAllCommentsAsync)
from weixin.views import weixin_api
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/$', IndexView.as_view(), name='index_page'),
    url(r'^$', IndexRedirectView.as_view(), name='index_redirect'),
    url(r'^blog/(?P<id>\d+)/$', ShowBlogView.as_view(), name='show_blog'),
    url(r'^blog/(?P<id>\d+)/comment/$', csrf_exempt(HandleCommentAsync.as_view()), name='handle_comment_async'),
    url(r'^blog/all_comments/$', GetAllCommentsAsync.as_view(), name='get_all_comments'),
    url(r'^tag_page/(?P<tag_name>.+)/$', ShowTagView.as_view(), name='show_tag'),

    url(r'^latest/feed/$', RSSFeed(), name='RSS_url'),

    url(r'^weixin/$', weixin_api, name='weixin_api'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )

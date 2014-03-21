#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import IndexPage, IndexPage2, blog_show, control_blog_show
from django_comments.feeds import LatestCommentFeed
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^index/$', IndexPage, name='indexpage'),
    url(r'^$', IndexPage2),
    url(r'^blog/(?P<id>\d+)/$', blog_show, name='detailblog'),#把这个url起别名为'detailblog'
    url(r'^control/$', control_blog_show, {'id': '1'}),
    url(r'^feeds/latest/$', LatestCommentFeed()),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
)

#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import index_page, index_page_2, blog_show
from django.contrib.auth.views import login, logout
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^index/$', index_page, name='indexpage'),
    url(r'^$', index_page_2),
    url(r'^blog/(?P<id>\d+)/$', blog_show, name='detailblog'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )

#coding=utf-8
from django.shortcuts import render_to_response
from blog.models import BlogPost
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers


def IndexPage(request):
    '''FrontPage function'''
    posts = BlogPost.objects.all()
    return render_to_response('index.html', {'posts': posts})


def IndexPage2(request):
    '''This function is for redirecting url from root to index/ '''
    return HttpResponseRedirect('/index/')


@cache_page(60 * 15)
@cache_control(public=True, must_revalidate=True, max_age=1200)#max_age是回应给浏览器的页面过期时间
@vary_on_headers('User-Agent')
def blog_show(request, id=''):
    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        raise Http404
    photos = post.photo_set.all()
    n = len(photos)
    paths = []
    i = 1
    while i<n+1:
        paths.append(photos.get(id=i).image.path)
        i += 1
    return render_to_response('blog_show.html',
                      {'post': post, 'paths': paths}
           )


def control_blog_show(request, id):
    rs = {}
    try:
        next_post = BlogPost.objects.get(id=int(id)+1)
        rs["next"] = next_post
    except BlogPost.DoesNotExist:
        rs["next"] = 0
    try:
        pre_post = BlogPost.objects.get(id=int(id)-1)
        rs["pre"] = pre_post
    except BlogPost.DoesNotExist:
        rs["pre"] = 0
    return render_to_response('blog_control.html',
                              {'next_post': rs["next"], 'pre_post': rs["pre"]}
           )

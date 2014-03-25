#coding=utf-8
from django.shortcuts import render
from blog.models import BlogPost
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers


@cache_page(60 * 15)
@cache_control(public=True, must_revalidate=True, max_age=1200)
def IndexPage(request):
    '''FrontPage function'''
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts},
           )


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
    blog_post_list = {}

    photos = post.photo_set.all()
    photos_num = len(photos)
    for i in xrange(photos_num):
        blog_post_list[photos[i].sequence] = photos[i]

    codes = post.code_set.all()
    codes_num = len(codes)
    for j in xrange(codes_num):
        blog_post_list[codes[i].sequence] = codes[j]

    paragraphs = post.paragraph_set.all()
    paragraphs_num = len(paragraphs)
    for k in xrange(paragraphs_num):
        blog_post_list[paragraphs[k].sequence] = paragraphs[k]

    context_list = []
    for x in sorted(blog_post_list):
        context_list.append(blog_post_list[x])

    return render(request, 'blog_show.html',
                            {'post': post,
                             'context_list': context_list,
                             },
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
    return render(request, 'blog_control.html',
                   {'next_post': rs["next"], 'pre_post': rs["pre"]},
           )

#coding=utf-8
from django.shortcuts import render
from blog.models import BlogPost
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers


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

    i = 1
    photos = post.photo_set.all()
    photos_num = len(photos)
    photos_paths = []
    while i < photos_num+1:
        photos_paths.append(photos.get(id=i).image.path)
        i += 1

    j = 1
    codes = post.code_set.all()
    codes_num = len(codes)
    codes_contents = []
    while j < codes_num+1:
        codes_contents.append(codes.get(id=j).content)
        j += 1

    return render(request, 'blog_show.html',
                            {'post': post,
                             'photos_paths': photos_paths,
                             'codes_contents': codes_contents
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

#coding=utf-8
from django.shortcuts import render
from blog.models import BlogPost
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.syndication.views import Feed


@cache_page(60 * 15)
@cache_control(public=True, must_revalidate=True, max_age=1200)
def index_page(request):
    '''这个view的功能是显示主页，并实现分页功能。
    cache_page装饰器定义了这个view所对应的页面的缓存时间。
    cache_control装饰器告诉了上游缓存可以以共缓存的形式缓存内容，并且告诉客户端浏览器，这个
    页面每次访问都要验证缓存，并且缓存有效时间为1200秒。
    '''
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts_of_page = paginator.page(page)
    except PageNotAnInteger:
        posts_of_page = paginator.page(1)
    except EmptyPage:
        posts_of_page = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts, 'posts_of_page': posts_of_page}, )


def index_page_2(request):
    '''这个view的作用是把指向站点根目录的请求重定向到/index/'''

    return HttpResponseRedirect('/index/')


@never_cache
def blog_show(request, id=''):
    '''这个view的作用是显示博客的正文内容。
    这个view会根据段落、图片、代码对象的sequence属性的值进行排序，
    生成一个最终显示列表返回给模版进行渲染。
    为了实现评论后刷新页面能马上看到评论信息，加入了nerver_cache装饰器使得这个
    view所对应的页面不被缓存。
    '''

    def post_objects(objects, output_dict):
        for i in xrange(len(objects)):
            output_dict[int('%d'%objects[i].sequence)] = objects[i]

    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        raise Http404
    blog_post_list = {}

    photos = post.photo_set.all()
    codes = post.code_set.all()
    paragraphs = post.paragraph_set.all()

    post_objects(photos, blog_post_list)
    post_objects(codes, blog_post_list)
    post_objects(paragraphs, blog_post_list)

    context_list = []
    for x in sorted(blog_post_list):
        context_list.append(blog_post_list[x])

    rs = {}
    try:
        next_post = BlogPost.objects.get(id=int(id)+1)
        rs['next'] = next_post
    except BlogPost.DoesNotExist:
        rs['next'] = 0
    try:
        pre_post = BlogPost.objects.get(id=int(id)-1)
        rs['pre'] = pre_post
    except BlogPost.DoesNotExist:
        rs['pre'] = 0

    return render(
        request, 'blog_show.html', {
          'post': post, 'context_list': context_list, 'next_post': rs['next'],
          'pre_post': rs['pre'],
        },
    )


class RSSFeed(Feed):
    '''实现RSS功能，按时间排序显示最新的5篇文章。'''

    title = "CJYFFF的简单博客"
    description = "反映CJYFFF博客的最新文章"
    link = "/blog/"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_description(self, item):
        return item.title

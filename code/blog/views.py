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
    '''
    这个view的功能是显示主页
    cache_page装饰器定义了这个view所对应的页面的缓存时间。
    cache_control装饰器告诉了客户端浏览器
    '''
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts},
           )


def index_page_2(request):
    '''
    这个view的作用是把指向站点根目录的请求重定向到/index/
    '''
    return HttpResponseRedirect('/index/')


@never_cache
def blog_show(request, id=''):
    '''
    为了实现评论后刷新页面能马上看到评论信息，加入了nerver_cache装饰器使得这个
    view所对应的页面不被缓存。
    '''
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
        blog_post_list[codes[j].sequence] = codes[j]

    paragraphs = post.paragraph_set.all()
    paragraphs_num = len(paragraphs)
    for k in xrange(paragraphs_num):
        blog_post_list[paragraphs[k].sequence] = paragraphs[k]

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

    return render(request, 'blog_show.html', {'post': post,
                                              'context_list': context_list,
                                              'next_post': rs['next'],
                                              'pre_post': rs['pre'],
                                             },
                 )


class RSSFeed(Feed):
    '''
    实现RSS功能，按时间排序显示最新的5篇文章。
    '''
    title = "CJYFFF的简单博客"
    description = "反映CJYFFF博客的最新文章"
    link = "/blog/"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_description(self, item):
        return item.title


'''
def msg_post(request):
    if request.method == 'POST':
        form = MsgPostForm(request.POST)
        if form.is_valid():
            newmessage = Msg(title=form.clean_data['title'],
                             content=form.clean_data['content'],
                             user=request.user,
                             ip=request.META['REMOTE_ADDR'],
                         )
        newmessage.save()
        return HttpResponseRedirect('/')
    else:
        form = MsgPostForm()
    return render(request, 'msg_post_page.html', {'form': form})
'''

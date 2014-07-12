#coding=utf-8
from django.shortcuts import render
from blog.models import BlogPost, Tag
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.syndication.views import Feed
from django.utils.functional import cached_property


@cache_page(60 * 15)
@cache_control(public=True, must_revalidate=True, max_age=1200)
def index_page(request):
    '''Index page view, this view also implement paginator function.'''
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    RANGE_MAX = 5
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts_of_page = paginator.page(page)
    except PageNotAnInteger:
        posts_of_page = paginator.page(1)
    except EmptyPage:
        posts_of_page = paginator.page(paginator.num_pages)

    tag_objects = ProcessTag()
    tag_list = tag_objects.count
    show_lastest_comment = ShowLastestComment()
    all_comments_list = show_lastest_comment.show

    page_range = paginator.page_range
    current_page = posts_of_page.number
    if len(page_range) > RANGE_MAX:
        if current_page > RANGE_MAX/2:
            border = page_range[-1] - current_page
            if border < RANGE_MAX/2:
                page_range = page_range[current_page - RANGE_MAX + border:]
            else:
                page_range = page_range[current_page - RANGE_MAX/2 - 1:current_page + RANGE_MAX/2 -1]
        else:
            page_range = page_range[:RANGE_MAX]

    return render(request, 'index.html', {
        'posts_of_page': posts_of_page,
        'tag_list': tag_list,
        'all_comments_list': all_comments_list,
        'page_range': page_range,
        },
    )


def index_page_2(request):
    '''Redirect '/' request to '/index/'.'''

    return HttpResponseRedirect('/index/')


@never_cache
def show_blog(request, id=''):
    '''This view is for showing articles of the blog.models.
    The functions of this views has:
    1 Showing the paragraphs, pictures and codes order by the their 'sequence'
      properties which are define in the models.
    2 Implementing links of the next\previous pages.
    '''

    def create_post_objects(objects, output_dict):
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

    create_post_objects(photos, blog_post_list)
    create_post_objects(codes, blog_post_list)
    create_post_objects(paragraphs, blog_post_list)

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

    tag_objects = ProcessTag()
    tag_list = tag_objects.count
    show_lastest_comment = ShowLastestComment()
    all_comments_list = show_lastest_comment.show

    return render(
        request, 'show_blog.html', {
            'post': post,
            'context_list': context_list,
            'next_post': rs['next'],
            'pre_post': rs['pre'],
            'tag_list': tag_list,
            'all_comments_list': all_comments_list,
        },
    )


class ProcessTag(object):

    def __init__(self):
        self.tags = Tag.objects.all()

    @cached_property
    def count(self):
        '''Generating the tag,
        and counting the amount of the articles of each tag.
        '''
        tag_list = {}
        for tag in self.tags:
            posts_of_tag = tag.blogpost_set.all()
            tag_amount = len(posts_of_tag)
            tag_list['%s' % tag.tag_name] = tag_amount
        return tag_list

    def show(self, request, tag_name):
        '''Generating the tag's page.'''
        for tag in self.tags:
            if tag.tag_name == tag_name:
                target_tag = tag
                break
        target_post = target_tag.blogpost_set.all()
        tag_list = self.count

        return render(request, 'tag_page.html', {
            'target_post': target_post,
            'tag_name': tag_name,
            'tag_list': tag_list,
            }, )


class ShowLastestComment(object):

    def __init__(self):
        from django_comments.forms import Comment
        self.all_comments = Comment.objects.all()

    @cached_property
    def show(self):
        '''Show the latest comments on the pages'''
        all_comments_list = []
        for comment in self.all_comments:
            submit_date = comment.submit_date
            name = comment.name
            content = comment.comment
            blog_title = BlogPost.objects.get(id=comment.object_pk).title
            blog_id = comment.object_pk
            all_comments_list.append([
                submit_date,
                name,
                content,
                blog_title,
                blog_id,
            ])
        all_comments_list = sorted(all_comments_list, key=lambda x: x[0],
            reverse=True)
        all_comments_list = all_comments_list[:10]
        return all_comments_list


class RSSFeed(Feed):
    '''Implementing the RSS function. Show the 5 of the latest articles.'''

    title = "CJYFFF的简单博客"
    description = "反映CJYFFF博客的最新文章"
    link = "/blog/"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_description(self, item):
        return item.title

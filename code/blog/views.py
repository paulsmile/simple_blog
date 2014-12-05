#! /usr/bin/env python
#coding=utf-8

from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.views.generic.base import View, ContextMixin, RedirectView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse

from blog.models import BlogPost, Tag, MyComment
from blog.forms import MyCommentForm

import json
import paho.mqtt.client as mqtt
from random import randint
import struct
import time



def render_json_response(ret, status=200, headers={}):
    resp = HttpResponse(json.dumps(ret), status=status, content_type='application/json')
    for k, v in headers.items():
        resp[k] = v
    return resp


def get_format_time(date_time):
    return '%s-%s-%s %s:%s' % (date_time.year, date_time.month, date_time.day,
                               date_time.hour, date_time.minute)



def get_gokit_led(level):

    did = "wz2TXX7UMnMqbqzrRiMBUL"
    client_id = "usr"+str(randint(0,1000000000))
    print client_id

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        pl = msg.payload
        print pl.encode('hex')
        print("on_message:"+msg.topic+" \n"+repr(msg.payload))

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def on_subscribe(client, userdata, mid, granted_qos):
        print("on_subscribe")

    def on_publish(client, userdata, mid):
        print 'on publish'

    try:
        client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.on_publish = on_publish

        client.username_pw_set("2$42a7563f305342ae805cbb21d968a0ce$a6f899f25e734fd58ff0fca1dae1388d", "ba4214b178d5449c894986b10f00f91d")
        client.connect("m2m.gizwits.com", 1883, 55)
    except KeyboardInterrupt:
        client.stop()

    topic = "dev2app/"+did
    print(topic)
    print client.subscribe(topic)
    topic = "app2dev/"+did+"/"+client_id
    if level == 1:
        array = bytearray(struct.pack('!LBBBBBBBBBBBB',3, ord('\x0b'), ord('\x00'),
                    ord('\x00'), ord('\x09'), ord('\x01'), ord('\x1c'), ord('\x00'), 128, ord('\x00'),  ord('\x00'), ord('\x00'), ord('\x00')))
        print client.publish(topic, array, retain=True)
    elif level == 2:
        array = bytearray(struct.pack('!LBBBBBBBBBBBB',3, ord('\x0b'), ord('\x00'),
                    ord('\x00'), ord('\x09'), ord('\x01'), ord('\x1c'), ord('\x00'), 128, ord('\x00'), 64, ord('\x00'), ord('\x00')))
        print client.publish(topic, array, retain=True)
    elif level == 3:
        array = bytearray(struct.pack('!LBBBBBBBBBBBB',3, ord('\x0b'), ord('\x00'),
                    ord('\x00'), ord('\x09'), ord('\x01'), ord('\x1c'), ord('\x00'), 4, 2, 1, ord('\x00'), ord('\x00')))
        print client.publish(topic, array, retain=True)

    time.sleep(1)
    client.loop(1)

class BaseView(ContextMixin, View):

    def __init__(self):
        super(BaseView, self).__init__()
        self.tags = Tag.objects.all()

    def count_tags(self):
        '''Generating the tag, and counting the amount of the articles of each tag.'''

        tags_list = {}
        for tag in self.tags:
            posts_of_tag = tag.blogpost_set.all()
            tag_amount = len(posts_of_tag)
            tags_list['%s' % tag.tag_name] = tag_amount
        return tags_list

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
            'tags_list': self.count_tags(),
        })

        return context


class IndexView(BaseView, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        context = super(IndexView, self).get_context_data(**kwargs)

        RANGE_MAX = 4
        posts = BlogPost.objects.all()
        paginator = Paginator(posts, 5)
        page = self.request.GET.get('page')

        try:
            posts_of_page = paginator.page(page)
        except PageNotAnInteger:
            posts_of_page = paginator.page(1)
        except EmptyPage:
            posts_of_page = paginator.page(paginator.num_pages)

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

        context.update({
            'posts_of_page': posts_of_page,
            'page_range': page_range,
        })

        return context


class IndexRedirectView(RedirectView):
    '''Redirect '/' request to '/index/'.'''

    url = reverse_lazy('index_page')


class ShowBlogView(BaseView, TemplateView):
    template_name = 'show_blog.html'

    def create_post_objects(self, objects, output_dict):
        for i in xrange(len(objects)):
            output_dict[int('%d'%objects[i].sequence)] = objects[i]

    def get_context_data(self, **kwargs):
        context = super(ShowBlogView, self).get_context_data(**kwargs)

        id = kwargs['id']

        post = get_object_or_404(BlogPost, id=id)

        blog_post_list = {}
        photos = post.photo_set.all()
        codes = post.code_set.all()
        paragraphs = post.paragraph_set.all()

        # Showing the paragraphs, pictures and codes order by the their 'sequence' properties
        # which are define in the models:
        self.create_post_objects(photos, blog_post_list)
        self.create_post_objects(codes, blog_post_list)
        self.create_post_objects(paragraphs, blog_post_list)

        context_list = []
        for x in sorted(blog_post_list):
            context_list.append(blog_post_list[x])

        # Implementing links of the next\previous pages:
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

        context.update({
            'post': post,
            'context_list': context_list,
            'next_post': rs['next'],
            'pre_post': rs['pre'],
        })
        return context


class HandleCommentAsync(View):

    def get(self, request, **kwargs):
        ret = {'comments': []}
        blog = get_object_or_404(BlogPost, id=kwargs['id'])
        get_comments = MyComment.objects.filter(blog=blog)

        for comment in get_comments.order_by('-created_at'):
            ret['comments'].append({
                'author': comment.author,
                'created_at': get_format_time(comment.created_at),
                'content': comment.content,
            })
        return render_json_response(ret, status=200)

    def post(self, request, **kwargs):
        ret = {}
        form = MyCommentForm(request.POST)
        if not form.is_valid():
            return render_json_response(ret, status=400)
        comment = form.save(commit=False)
        blog = get_object_or_404(BlogPost, id=kwargs['id'])
        comment.blog = blog
        comment.save()
        return render_json_response(ret, status=201)


class GetAllCommentsAsync(View):

    def get(self, request, **kwargs):
        ret = {'comments': []}
        all_comments = MyComment.objects.all().order_by('-created_at')[:5]

        for comment in all_comments:
            ret['comments'].append({
                'author': comment.author,
                'created_at': get_format_time(comment.created_at),
                'content': comment.content,
                'blog_id': comment.blog.id,
                'blog_title': comment.blog.title,
            })
        return render_json_response(ret, status=200)


class ShowTagView(BaseView, TemplateView):
    '''Generating the tag's page.'''
    template_name = 'show_tag.html'

    def get_context_data(self, **kwargs):
        context = super(ShowTagView, self).get_context_data(**kwargs)
        tag_name = kwargs['tag_name']
        tags = Tag.objects.all()
        for tag in tags:
            if tag.tag_name == tag_name:
                target_tag = tag
                break
        target_post = target_tag.blogpost_set.all()

        context.update({'target_post': target_post, 'tag_name': tag_name, })
        return context


class RSSFeed(Feed):
    '''Implementing the RSS function. Show the 5 of the latest articles.'''

    title = "CJYFFF的简单博客"
    description = "反映CJYFFF博客的最新文章"
    link = "/blog/"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return settings.DOMAIN + reverse('show_blog', kwargs={'id': item.id})


class GokitGetWeather(TemplateView):
    template_name = 'gokit/get_weather.html'


class GokitGetWeatherAsync(View):

    def get(self, request, **kwargs):
        import requests
        city = request.GET.get('city')
        url = 'http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=5slgyqGDENN7Sy7pw29IUvrZ' % city
        r = requests.get(url)
        weather_data = json.loads(r.content)['results'][0]['weather_data']
        # torrow weather
        t_weather_data = weather_data[0]['weather']

        if t_weather_data.find(u'晴'):
            weather_info = 1
        elif t_weather_data.find(u'多云'):
            weather_info = 2
        elif t_weather_data.find(u'雨'):
            weather_info = 3
        else:
            weather_info = 4
        get_gokit_led(weather_info)
        ret = {'weather_info': weather_info}
        return render_json_response(ret, status=200)

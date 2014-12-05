#! /usr/bin/env python
#coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse

from blog.factories import BlogPostFactory, CommentFactory

import json


class HandleCommentAsyncTest(TestCase):

    def setUp(self):
        self.blog = BlogPostFactory()
        self.url = reverse('handle_comment_async', kwargs={'id': self.blog.id})

    def test_comment(self):
        # post currect data:
        d = {
            'author': 'cjyfff',
            'author_email': '110@123.com',
            'content': 'xxx',
        }
        resp = self.client.post(self.url, d)
        self.assertEqual(resp.status_code, 201)

        # post wrong data:
        d = {
            'author': 'cjyfff',
            'author_email': '110',
            'content': 'xxx',
        }
        resp = self.client.post(self.url, d)
        self.assertEqual(resp.status_code, 400)

        # get comments' data
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        comments = json.loads(resp.content)['comments']
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]['author'], 'cjyfff')


class GetAllCommentsAsyncTest(TestCase):

    def setUp(self):
        self.url = reverse('get_all_comments')
        for i in xrange(5):
            CommentFactory()

    def test_get_all_comments(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        comments = json.loads(resp.content)['comments']
        self.assertEqual(len(comments), 5)


class GokitGetWeather(TestCase):

    def setUp(self):
        self.url = reverse('gokit_get_weather_async')

    def test_get_weather(self):
        d = {'city': u'北京'}
        resp = self.client.post(self.url, d)
        resp = json.loads(resp.content)
        self.assertTrue('weather_info' in resp)

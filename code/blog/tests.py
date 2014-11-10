#! /usr/bin/env python
#coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from blog.models import BlogPost

from uuid import uuid4
from datetime import datetime

import json


def random_data(length=None):
    if length:
        return uuid4().hex[:length]
    return uuid4().hex[:30]


class BlogPostFactory(object):

    @classmethod
    def get_object(self):
        blog_post = BlogPost(
            title=random_data(),
            author=random_data(),
            summary=random_data(),
            timestamp=datetime.now(),
        )
        blog_post.save()
        return blog_post


class HandleCommentAsyncTest(TestCase):

    def setUp(self):
        self.blog = BlogPostFactory.get_object()
        self.url = reverse('handle_comment_async', kwargs={'id': self.blog.id})

    def test_comment(self):
        # post currect data:
        d = {
            'author': 'cjyfff',
            'author_email': '110@123.com',
            'content': 'xxx'
        }
        resp = self.client.post(self.url, d)
        self.assertEqual(resp.status_code, 201)

        # post wrong data:
        d = {
            'author': 'cjyfff',
            'author_email': '110',
            'content': 'xxx'
        }
        resp = self.client.post(self.url, d)
        self.assertEqual(resp.status_code, 400)

        # get comments' data
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        comments = json.loads(resp.content)['comments']
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]['author'], 'cjyfff')

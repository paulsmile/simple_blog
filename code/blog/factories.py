#! /usr/bin/env python
#coding=utf-8
import factory
from blog.models import BlogPost, MyComment


class BlogPostFactory(factory.DjangoModelFactory):

    class Meta:
        model = BlogPost


class CommentFactory(factory.DjangoModelFactory):

    class Meta:
        model = MyComment

    blog = factory.SubFactory(BlogPostFactory)

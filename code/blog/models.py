#coding=utf-8
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name


class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    tag = models.ManyToManyField(Tag, blank=True)
    summary = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.timestamp)

    class Meta(object):
        ordering = ['-timestamp']


# The classes of Paragraph、Photo、Code have properties named 'sequence',
# which are stand for the sequence when they are shown in the articles.

class Paragraph(models.Model):
    discern = "paragraph"
    sequence = models.PositiveSmallIntegerField()
    describe = models.CharField(max_length=100)
    tag = models.ManyToManyField(BlogPost)
    paragraph = models.TextField()

    def __unicode__(self):
        return self.describe


class Photo(models.Model):
    discern = "photo"
    sequence = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    #image = models.ImageField(upload_to='photos', blank=True)
    tag = models.ManyToManyField(BlogPost)
    url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Code(models.Model):
    discern = "code"
    sequence = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=150)
    tag = models.ManyToManyField(BlogPost)
    content = models.TextField()

    def __unicode__(self):
        return self.title


class MyComment(models.Model):
    author = models.CharField(max_length=32)
    author_email = models.EmailField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost)

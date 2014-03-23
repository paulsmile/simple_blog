#coding=utf-8
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name


class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.timestamp)

    class Meta(object):
        ordering = ['-timestamp']

    @models.permalink
    def get_absolute_url(self):
        return ('detailblog', None, {'object_id': self.id})


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos')
    tag = models.ManyToManyField(BlogPost, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detailblog', None, {'object_id': self.id})


class Code(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    tag = models.ManyToManyField(BlogPost, blank=True)

    def __unicode__(self):
        return self.title

#coding=utf-8
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name


class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    summary = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.timestamp)

    class Meta(object):
        ordering = ['-timestamp']


class Paragraph(models.Model):
    discern = "paragraph"
    sequence = models.PositiveSmallIntegerField()
    tag = models.ManyToManyField(BlogPost)
    paragraph = models.TextField()


class Photo(models.Model):
    discern = "photo"
    sequence = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos')
    tag = models.ManyToManyField(BlogPost)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detailblog', None, {'object_id': self.id})


class Code(models.Model):
    discern = "code"
    sequence = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=150)
    content = models.TextField()
    tag = models.ManyToManyField(BlogPost)

    def __unicode__(self):
        return self.title

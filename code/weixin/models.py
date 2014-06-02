#coding=utf-8
from django.db import models


class WeixinClientUser(models.Model):
    UserName = models.CharField(max_length=50)

'''
class WeixinClientMsg(models.Model):
    UserName = models.ForeignKey(WeixinClientUser)
    CreateTime = models.IntegerField()
    MsgType = models.CharField(max_length=20)
    Event = models.CharField(max_length=20, blank=True)
    EventKey = models.CharField(max_length=100)
    Ticket = models.CharField(max_length=100)
'''

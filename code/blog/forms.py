#! /usr/bin/env python
#coding=utf-8
from django import forms
from django_comments.forms import CommentForm
from captcha.fields import CaptchaField


class MyComment(CommentForm):
    name = forms.CharField(label='您的名字', max_length=50)
    email = forms.EmailField(label='您的Email地址')
    url = forms.URLField(label='您的个人主页(可不填)', required=False)
    comment = forms.CharField(label='您的评论', widget=forms.Textarea,
                                    max_length=10000)
    honeypot = forms.CharField(required=False,
                    label='这是防止恶意自动提交评论用的，请不要在此栏填写内容')
    captcha = CaptchaField(label='验证码')

    def get_comment_create_data(self):
        data = super(MyComment, self).get_comment_create_data()
        return data
